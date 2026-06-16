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
from datetime import datetime, timedelta
import time
import logging

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
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _safe_download(tickers: list[str], period: str = "6mo", interval: str = "1d") -> dict[str, pd.DataFrame]:
    """Download OHLCV for a batch of tickers; return {ticker: df}."""
    if not tickers:
        return {}
    try:
        raw = yf.download(
            tickers,
            period=period,
            interval=interval,
            group_by="ticker",
            auto_adjust=True,
            threads=True,
            progress=False,
        )
    except Exception as e:
        logger.warning(f"Download error: {e}")
        return {}

    result = {}
    if len(tickers) == 1:
        # single ticker — yfinance returns flat df
        t = tickers[0]
        if not raw.empty:
            result[t] = raw.copy()
    else:
        for t in tickers:
            try:
                df = raw[t].dropna(how="all")
                if len(df) >= 50:
                    result[t] = df
            except Exception:
                pass
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

BATCH_SIZE = 50   # tickers per yfinance call

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
                # fetch company name
                name = ticker
                try:
                    info = yf.Ticker(ticker).fast_info
                    name = getattr(info, "display_name", ticker) or ticker
                except Exception:
                    pass

                hits.append({
                    "Ticker":             ticker,
                    "Naam":               name,
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

        # small pause to be polite to Yahoo
        time.sleep(0.3)

    df_hits = pd.DataFrame(hits)
    if not df_hits.empty:
        df_hits = df_hits.sort_values("RSI (14)").reset_index(drop=True)
    return df_hits


# ─────────────────────────────────────────────────────────────────────────────
# Single-ticker chart data
# ─────────────────────────────────────────────────────────────────────────────

def get_chart_data(ticker: str, period: str = "6mo") -> pd.DataFrame | None:
    """Return OHLCV + RSI + SMA50 + support for a single ticker."""
    data = _safe_download([ticker], period=period)
    if ticker not in data:
        return None
    df = data[ticker].copy()
    if len(df) < 20:
        return None
    df["RSI"]     = rsi(df["Close"], length=14)
    df["SMA50"]   = sma(df["Close"], length=50)
    df["SMA20"]   = sma(df["Close"], length=20)
    df["Support"] = df["Low"].rolling(20).min().shift(1)
    return df
