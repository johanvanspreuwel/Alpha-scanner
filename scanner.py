"""
scanner.py — Alpha Scanner core logic
Criteria (from strategy description):
  • Bodem-fase (bottom / accumulation phase)
  • RSI ≤ 45
  • Koers 0 – 5 % above support level
  • Volume ≥ 0.8× 20-day average  (low volume = accumulation)
"""

import yfinance as yf
import pandas as pd
import numpy as np
import requests
from io import StringIO
from datetime import datetime, timedelta
import time
import logging

from tickers import get_company_name

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Indicator math (pure pandas/numpy — no compiled dependencies)
# ─────────────────────────────────────────────────────────────────────────────

def rsi(series: pd.Series, length: int = 14) -> pd.Series:
    """Wilder's RSI, pure pandas implementation."""
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1 / length, min_periods=length, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / length, min_periods=length, adjust=False).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    out = 100 - (100 / (1 + rs))
    out = out.where(avg_loss != 0, 100)  # all gains -> RSI 100
    return out


def sma(series: pd.Series, length: int) -> pd.Series:
    return series.rolling(length).mean()


# ─────────────────────────────────────────────────────────────────────────────
# Stooq data source (primary) — free, no API key, no aggressive rate limiting
# ─────────────────────────────────────────────────────────────────────────────

# Map our Yahoo-style exchange suffix to Stooq's country-code suffix.
_YAHOO_TO_STOOQ_SUFFIX = {
    "":     "us",   # no suffix -> US ticker (NYSE/Nasdaq)
    ".AS":  "nl",
    ".DE":  "de",
    ".PA":  "fr",
    ".L":   "uk",
    ".MC":  "es",
    ".SW":  "ch",
    ".BR":  "be",
    ".ST":  "se",
    ".HE":  "fi",
    ".CO":  "dk",
    ".LS":  "pt",
    ".VI":  "at",
    ".MI":  "it",
}

_STOOQ_SESSION = requests.Session()
_STOOQ_SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
})
_stooq_warmed_up = False


def _warm_up_stooq_session():
    """Visit Stooq's homepage once to pick up the consent cookie European
    visitors need before the CSV endpoint serves real data. Best-effort —
    failures are silently ignored since the download call has its own
    timeout and error handling."""
    global _stooq_warmed_up
    if _stooq_warmed_up:
        return
    try:
        _STOOQ_SESSION.get("https://stooq.com/", timeout=5)
    except Exception:
        pass
    _stooq_warmed_up = True


def _yahoo_ticker_to_stooq(ticker: str) -> str:
    """Convert a Yahoo-style ticker (e.g. 'ASML.AS', 'AAPL') to Stooq format
    (e.g. 'asml.nl', 'aapl.us')."""
    for suffix, stooq_suffix in _YAHOO_TO_STOOQ_SUFFIX.items():
        if suffix and ticker.endswith(suffix):
            base = ticker[: -len(suffix)]
            return f"{base.replace('-', '_').replace('.', '-').lower()}.{stooq_suffix}"
    # No recognized suffix -> assume US ticker
    return f"{ticker.replace('-', '_').lower()}.us"


def _stooq_download_one(ticker: str, period: str = "6mo") -> pd.DataFrame | None:
    """Download daily OHLCV for a single ticker from Stooq. Returns None on failure."""
    stooq_symbol = _yahoo_ticker_to_stooq(ticker)

    period_days = {
        "1mo": 35, "3mo": 100, "6mo": 200, "1y": 400, "2y": 760,
    }.get(period, 200)
    end = datetime.today()
    start = end - timedelta(days=period_days)

    url = (
        f"https://stooq.com/q/d/l/?s={stooq_symbol}"
        f"&d1={start:%Y%m%d}&d2={end:%Y%m%d}&i=d"
    )

    try:
        resp = _STOOQ_SESSION.get(url, timeout=8)
        if resp.status_code != 200:
            return None
        text = resp.text.strip()
        # Stooq returns a plain "No data" or HTML on failure
        if not text or text.startswith("<") or "No data" in text[:50]:
            return None

        df = pd.read_csv(StringIO(text), parse_dates=["Date"])
        if df.empty or "Close" not in df.columns:
            return None
        df = df.set_index("Date").sort_index()
        # Normalize column names to match yfinance convention
        df = df.rename(columns={
            "Open": "Open", "High": "High", "Low": "Low",
            "Close": "Close", "Volume": "Volume",
        })
        return df
    except Exception as e:
        logger.debug(f"Stooq fout voor {ticker} ({stooq_symbol}): {e}")
        return None


def _stooq_download_batch(
    tickers: list[str],
    period: str = "6mo",
    min_rows: int = 50,
    pause: float = 0.15,
) -> dict[str, pd.DataFrame]:
    """Download a batch of tickers from Stooq one by one (Stooq has no
    multi-ticker bulk endpoint, but is far more forgiving on request rate
    than Yahoo)."""
    _warm_up_stooq_session()
    result = {}
    for t in tickers:
        df = _stooq_download_one(t, period=period)
        if df is not None and len(df) >= min_rows:
            result[t] = df
        time.sleep(pause)
    return result


# ─────────────────────────────────────────────────────────────────────────────
# Yahoo Finance via yfinance (fallback for tickers Stooq doesn't have)
# ─────────────────────────────────────────────────────────────────────────────

def _yfinance_download(
    tickers: list[str],
    period: str = "6mo",
    interval: str = "1d",
    max_retries: int = 2,
    min_rows: int = 50,
) -> dict[str, pd.DataFrame]:
    """Download OHLCV for a batch of tickers via yfinance; return {ticker: df}.
    Retries with backoff on rate-limit errors."""
    if not tickers:
        return {}

    raw = None
    for attempt in range(max_retries):
        try:
            raw = yf.download(
                tickers,
                period=period,
                interval=interval,
                group_by="ticker",
                auto_adjust=True,
                threads=False,
                progress=False,
            )
            break
        except Exception as e:
            wait = 5 * (attempt + 1)
            logger.warning(f"yfinance fout (poging {attempt + 1}/{max_retries}): {e}. Wachten {wait}s…")
            time.sleep(wait)

    if raw is None or raw.empty:
        return {}

    result = {}
    if isinstance(raw.columns, pd.MultiIndex):
        level0_values = set(raw.columns.get_level_values(0))
        ohlcv_fields = {"Open", "High", "Low", "Close", "Volume", "Adj Close"}
        if level0_values & ohlcv_fields:
            raw = raw.swaplevel(0, 1, axis=1)
        for t in tickers:
            try:
                df = raw[t].dropna(how="all")
                if len(df) >= min_rows and "Close" in df.columns:
                    result[t] = df
            except Exception:
                pass
    else:
        t = tickers[0]
        df = raw.dropna(how="all")
        if len(df) >= min_rows and "Close" in df.columns:
            result[t] = df
    return result


# ─────────────────────────────────────────────────────────────────────────────
# Combined data fetch: Stooq first, yfinance fallback for misses
# ─────────────────────────────────────────────────────────────────────────────

def _safe_download(
    tickers: list[str],
    period: str = "6mo",
    interval: str = "1d",
    min_rows: int = 50,
    use_yfinance_fallback: bool = True,
) -> dict[str, pd.DataFrame]:
    """Fetch OHLCV for `tickers`, trying Stooq first (no rate limits) and
    falling back to yfinance only for tickers Stooq couldn't provide."""
    if not tickers:
        return {}

    result = _stooq_download_batch(tickers, period=period, min_rows=min_rows)

    missing = [t for t in tickers if t not in result]
    if missing and use_yfinance_fallback:
        fallback = _yfinance_download(missing, period=period, interval=interval, min_rows=min_rows)
        result.update(fallback)

    return result


def _find_support(df: pd.DataFrame, window: int = 20) -> float:
    """
    Support = lowest low of the last `window` bars, smoothed slightly.
    We use the rolling minimum of the Low column.
    """
    if len(df) < window:
        return float(df["Low"].min())
    return float(df["Low"].rolling(window).min().iloc[-1])


def _calc_indicators(df: pd.DataFrame) -> dict | None:
    """
    Calculate RSI, volume ratio, support, and price-vs-support.
    Returns None if data is insufficient.
    """
    if len(df) < 50:
        return None

    close = df["Close"]
    low   = df["Low"]
    vol   = df["Volume"]

    # RSI (14)
    rsi_series = rsi(close, length=14)
    if rsi_series is None or rsi_series.dropna().empty:
        return None
    rsi_val = float(rsi_series.iloc[-1])

    # Volume ratio vs 20-day average
    vol_avg = float(vol.rolling(20).mean().iloc[-1])
    vol_now = float(vol.iloc[-1])
    vol_ratio = vol_now / vol_avg if vol_avg > 0 else 0.0

    # Support level (lowest low of last 20 bars, excluding today)
    support = _find_support(df.iloc[:-1], window=20)  # exclude current bar

    # Current price
    price = float(close.iloc[-1])

    # Price vs support (%)
    pct_above_support = ((price - support) / support * 100) if support > 0 else 999.0

    # 52-week high/low for context
    high_52w = float(close.tail(252).max())
    low_52w  = float(close.tail(252).min())

    # Simple trend context: SMA50 slope
    sma50 = sma(close, length=50)
    sma50_slope = None
    if sma50 is not None and len(sma50.dropna()) >= 5:
        sma50_slope = float(sma50.iloc[-1]) - float(sma50.iloc[-5])

    # Previous close for daily change
    prev_close = float(close.iloc[-2]) if len(close) >= 2 else price
    daily_change_pct = (price - prev_close) / prev_close * 100

    return {
        "price":              price,
        "rsi":                round(rsi_val, 1),
        "vol_ratio":          round(vol_ratio, 2),
        "support":            round(support, 4),
        "pct_above_support":  round(pct_above_support, 2),
        "high_52w":           round(high_52w, 4),
        "low_52w":            round(low_52w, 4),
        "sma50_slope":        round(sma50_slope, 4) if sma50_slope is not None else None,
        "daily_change_pct":   round(daily_change_pct, 2),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Alpha Scanner conditions
# ─────────────────────────────────────────────────────────────────────────────

def alpha_conditions(ind: dict, params: dict) -> tuple[bool, list[str]]:
    """
    Check Alpha Scanner criteria.
    Returns (passed: bool, reasons: list[str]).

    Criteria:
      1. RSI ≤ params['rsi_max']  (default 45)
      2. Price 0 – params['pct_above_max'] % above support  (default 5 %)
      3. Volume ≥ params['vol_min_ratio'] × 20-day avg  (default 0.8×)
    """
    reasons = []
    passed  = True

    rsi_max       = params.get("rsi_max", 45)
    pct_above_max = params.get("pct_above_max", 5.0)
    vol_min       = params.get("vol_min_ratio", 0.8)

    if ind["rsi"] > rsi_max:
        passed = False
        reasons.append(f"RSI {ind['rsi']} > {rsi_max}")

    if ind["pct_above_support"] < 0:
        passed = False
        reasons.append(f"Prijs {ind['pct_above_support']:.1f}% ONDER support")
    elif ind["pct_above_support"] > pct_above_max:
        passed = False
        reasons.append(f"Prijs {ind['pct_above_support']:.1f}% boven support (max {pct_above_max}%)")

    if ind["vol_ratio"] < vol_min:
        passed = False
        reasons.append(f"Volume ratio {ind['vol_ratio']:.2f} < {vol_min}")

    return passed, reasons


# ─────────────────────────────────────────────────────────────────────────────
# Main scan function
# ─────────────────────────────────────────────────────────────────────────────

BATCH_SIZE = 25   # tickers per batch (mainly relevant for yfinance fallback)

def run_alpha_scan(
    tickers: list[str],
    params: dict,
    progress_callback=None,
) -> pd.DataFrame:
    """
    Scan `tickers` for Alpha Scanner conditions.
    Returns DataFrame of hits sorted by RSI ascending.

    progress_callback(done: int, total: int) — optional UI hook.
    """
    hits   = []
    total  = len(tickers)
    done   = 0

    batches = [tickers[i:i + BATCH_SIZE] for i in range(0, total, BATCH_SIZE)]

    for batch in batches:
        data = _safe_download(batch)

        for ticker, df in data.items():
            ind = _calc_indicators(df)
            if ind is None:
                done += 1
                continue

            passed, reasons = alpha_conditions(ind, params)
            if passed:
                hits.append({
                    "Ticker":             ticker,
                    "Naam":               get_company_name(ticker),
                    "Prijs":              ind["price"],
                    "RSI (14)":           ind["rsi"],
                    "Vol ratio":          ind["vol_ratio"],
                    "Support":            ind["support"],
                    "% boven support":    ind["pct_above_support"],
                    "Dag wijziging %":    ind["daily_change_pct"],
                    "52w Hoog":           ind["high_52w"],
                    "52w Laag":           ind["low_52w"],
                    "SMA50 helling":      ind["sma50_slope"],
                })
            done += 1

        if progress_callback:
            progress_callback(done, total)

    df_hits = pd.DataFrame(hits)
    if not df_hits.empty:
        df_hits = df_hits.sort_values("RSI (14)").reset_index(drop=True)
    return df_hits


# ─────────────────────────────────────────────────────────────────────────────
# Single-ticker chart data
# ─────────────────────────────────────────────────────────────────────────────

def get_chart_data(ticker: str, period: str = "6mo") -> pd.DataFrame | None:
    """Return OHLCV + RSI + SMA50 + support for a single ticker."""
    data = _safe_download([ticker], period=period, min_rows=15)
    if ticker not in data:
        return None
    df = data[ticker].copy()
    if len(df) < 15:
        return None
    df["RSI"]     = rsi(df["Close"], length=14)
    df["SMA50"]   = sma(df["Close"], length=50)
    df["SMA20"]   = sma(df["Close"], length=20)
    df["Support"] = df["Low"].rolling(20).min().shift(1)
    return df
