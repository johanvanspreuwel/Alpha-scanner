"""
Alpha Scanner — Streamlit UI
Zoekt naar aandelen in een kortstondige dip (bodemfase / accumulatiefase).
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime

from tickers import get_universe, ALL_EXCHANGES
from scanner import run_alpha_scan, get_chart_data

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Alpha Scanner",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Dark terminal / trading-desk feel */
[data-testid="stAppViewContainer"] {
    background: #0d1117;
    color: #e6edf3;
}
[data-testid="stSidebar"] {
    background: #161b22;
    border-right: 1px solid #30363d;
}
[data-testid="stHeader"] { background: transparent; }

/* Title area */
.scanner-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 1rem 0 0.5rem;
    border-bottom: 1px solid #21262d;
    margin-bottom: 1.2rem;
}
.scanner-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.7rem;
    font-weight: 700;
    color: #58a6ff;
    letter-spacing: -0.5px;
}
.scanner-subtitle {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    color: #8b949e;
    margin-top: 2px;
}
.badge {
    display: inline-block;
    background: #1f6feb22;
    border: 1px solid #1f6feb;
    color: #58a6ff;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 0.72rem;
    font-family: 'IBM Plex Mono', monospace;
}
/* Metric cards */
.metric-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 14px 18px;
    text-align: center;
}
.metric-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #58a6ff;
    font-family: 'IBM Plex Mono', monospace;
}
.metric-label {
    font-size: 0.72rem;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 1px;
}
/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid #30363d;
    border-radius: 6px;
}
/* Sidebar labels */
.sidebar-section {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 1rem 0 0.4rem;
}
/* Condition pills in sidebar */
.cond-pill {
    background: #0d4a2e;
    border: 1px solid #238636;
    color: #3fb950;
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.72rem;
    font-family: 'IBM Plex Mono', monospace;
    display: inline-block;
    margin: 2px 2px;
}
</style>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)


# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="scanner-header">
  <div>
    <div class="scanner-title">🔎 Alpha Scanner</div>
    <div class="scanner-subtitle">
      Bodemfase · RSI ≤ 45 · Koers 0–5 % boven support · Volume ≥ 0.8×
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuratie")

    st.markdown('<div class="sidebar-section">📋 Beurzen</div>', unsafe_allow_html=True)
    selected_exchanges = st.multiselect(
        "Selecteer markten",
        options=ALL_EXCHANGES,
        default=["S&P 500", "S&P 400 MidCap", "AEX", "DAX", "CAC 40"],
        label_visibility="collapsed",
    )

    st.markdown('<div class="sidebar-section">🎛️ Scanner parameters</div>', unsafe_allow_html=True)

    rsi_max = st.slider(
        "RSI maximaal",
        min_value=20, max_value=60, value=45, step=1,
        help="Aandelen met RSI ≤ deze waarde worden meegenomen (oververkocht / dip).",
    )

    pct_above_max = st.slider(
        "Max % boven support",
        min_value=0.5, max_value=10.0, value=5.0, step=0.5,
        help="Prijs moet binnen dit percentage boven de support zitten.",
    )

    vol_min_ratio = st.slider(
        "Min volume-ratio (×20d gem)",
        min_value=0.3, max_value=2.0, value=0.8, step=0.1,
        help="Volume ≥ X × 20-daags gemiddelde. Laag volume = accumulatie.",
    )

    st.markdown('<div class="sidebar-section">ℹ️ Actieve strategie</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div>
      <span class="cond-pill">RSI ≤ {rsi_max}</span>
      <span class="cond-pill">0–{pct_above_max}% boven sup.</span>
      <span class="cond-pill">vol ≥ {vol_min_ratio}×</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    scan_btn = st.button("▶  Start scan", type="primary", use_container_width=True)

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.68rem;color:#8b949e'>"
        "Data via Yahoo Finance · Geen beleggingsadvies"
        "</div>",
        unsafe_allow_html=True,
    )


# ─── Session state ────────────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results    = None
if "scan_time" not in st.session_state:
    st.session_state.scan_time  = None
if "ticker_count" not in st.session_state:
    st.session_state.ticker_count = 0


# ─── Scan ─────────────────────────────────────────────────────────────────────
if scan_btn:
    if not selected_exchanges:
        st.warning("Selecteer minimaal één beurs.")
    else:
        universe = get_universe(selected_exchanges)
        total    = len(universe)
        params   = {
            "rsi_max":        rsi_max,
            "pct_above_max":  pct_above_max,
            "vol_min_ratio":  vol_min_ratio,
        }

        st.session_state.ticker_count = total

        progress_bar  = st.progress(0, text=f"Initialiseren… 0/{total}")
        status_text   = st.empty()

        def update_progress(done: int, total: int):
            pct = done / total
            progress_bar.progress(pct, text=f"Scannen… {done}/{total} tickers")

        t0 = time.time()
        results = run_alpha_scan(universe, params, progress_callback=update_progress)
        elapsed = time.time() - t0

        progress_bar.empty()
        status_text.empty()

        st.session_state.results   = results
        st.session_state.scan_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        st.session_state.elapsed   = round(elapsed, 1)


# ─── Results ──────────────────────────────────────────────────────────────────
results = st.session_state.results

if results is not None:
    n_hits = len(results)
    total  = st.session_state.ticker_count

    # ── Metrics row ──────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-value">{n_hits}</div>
          <div class="metric-label">Hits</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-value">{total}</div>
          <div class="metric-label">Gescande tickers</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        hit_pct = round(n_hits / total * 100, 1) if total else 0
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-value">{hit_pct}%</div>
          <div class="metric-label">Hitrate</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-value">{st.session_state.get('elapsed','–')}s</div>
          <div class="metric-label">Scanduur</div>
        </div>""", unsafe_allow_html=True)

    st.markdown(
        f"<div style='font-size:0.73rem;color:#8b949e;margin:0.5rem 0 1rem'>"
        f"Laatste scan: {st.session_state.scan_time}</div>",
        unsafe_allow_html=True,
    )

    if n_hits == 0:
        st.info("Geen aandelen gevonden die aan alle Alpha Scanner-criteria voldoen. "
                "Probeer de parameters te verruimen of meer beurzen te selecteren.")
    else:
        # ── Tabs: table + chart ───────────────────────────────────────────────
        tab_list, tab_chart = st.tabs(["📋 Resultatenlijst", "📈 Grafiek"])

        with tab_list:
            display_df = results.copy()

            # Colour RSI column
            def style_rsi(val):
                if val <= 30:  return "color:#ff7b72; font-weight:700"
                if val <= 45:  return "color:#ffa657"
                return ""

            def style_vol(val):
                if val < 0.8: return "color:#8b949e"
                return "color:#3fb950"

            styled = (
                display_df.style
                .applymap(style_rsi, subset=["RSI (14)"])
                .applymap(style_vol, subset=["Vol ratio"])
                .format({
                    "Prijs":           "{:.2f}",
                    "RSI (14)":        "{:.1f}",
                    "Vol ratio":       "{:.2f}×",
                    "Support":         "{:.2f}",
                    "% boven support": "{:.2f}%",
                    "Dag wijziging %": "{:+.2f}%",
                    "52w Hoog":        "{:.2f}",
                    "52w Laag":        "{:.2f}",
                })
            )

            st.dataframe(styled, use_container_width=True, height=450)

            # Download CSV
            csv = results.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️  Download CSV",
                data=csv,
                file_name=f"alpha_scan_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
            )

        with tab_chart:
            ticker_options = results["Ticker"].tolist()
            selected_ticker = st.selectbox(
                "Selecteer een aandeel voor de grafiek",
                options=ticker_options,
                index=0,
            )

            period_map = {"1 maand": "1mo", "3 maanden": "3mo",
                          "6 maanden": "6mo", "1 jaar": "1y"}
            period_label = st.radio(
                "Periode", list(period_map.keys()), index=2, horizontal=True
            )
            period = period_map[period_label]

            with st.spinner(f"Grafiekdata ophalen voor {selected_ticker}…"):
                chart_df = get_chart_data(selected_ticker, period=period)

            if chart_df is None:
                st.error("Kon geen data ophalen voor dit aandeel.")
            else:
                # ── Plotly chart ─────────────────────────────────────────────
                fig = make_subplots(
                    rows=2, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.06,
                    row_heights=[0.7, 0.3],
                    subplot_titles=(
                        f"{selected_ticker} — Koers + Support + SMA",
                        "RSI (14)",
                    ),
                )

                # Candlestick
                fig.add_trace(go.Candlestick(
                    x=chart_df.index,
                    open=chart_df["Open"],
                    high=chart_df["High"],
                    low=chart_df["Low"],
                    close=chart_df["Close"],
                    name="Koers",
                    increasing_fillcolor="#238636",
                    increasing_line_color="#238636",
                    decreasing_fillcolor="#da3633",
                    decreasing_line_color="#da3633",
                ), row=1, col=1)

                # Support line
                if "Support" in chart_df.columns:
                    fig.add_trace(go.Scatter(
                        x=chart_df.index,
                        y=chart_df["Support"],
                        name="Support (20d low)",
                        line=dict(color="#ffa657", width=1.5, dash="dot"),
                    ), row=1, col=1)

                # SMA50
                if "SMA50" in chart_df.columns:
                    fig.add_trace(go.Scatter(
                        x=chart_df.index,
                        y=chart_df["SMA50"],
                        name="SMA 50",
                        line=dict(color="#58a6ff", width=1.2),
                    ), row=1, col=1)

                # SMA20
                if "SMA20" in chart_df.columns:
                    fig.add_trace(go.Scatter(
                        x=chart_df.index,
                        y=chart_df["SMA20"],
                        name="SMA 20",
                        line=dict(color="#bc8cff", width=1, dash="dash"),
                    ), row=1, col=1)

                # RSI
                if "RSI" in chart_df.columns:
                    fig.add_trace(go.Scatter(
                        x=chart_df.index,
                        y=chart_df["RSI"],
                        name="RSI (14)",
                        line=dict(color="#ffa657", width=1.5),
                        fill="tozeroy",
                        fillcolor="rgba(255,166,87,0.08)",
                    ), row=2, col=1)

                    # RSI threshold lines
                    for level, colour, label in [
                        (45, "#ffa657", "RSI 45"),
                        (30, "#ff7b72", "Oversold 30"),
                        (70, "#3fb950", "Overbought 70"),
                    ]:
                        fig.add_hline(
                            y=level, line_dash="dot",
                            line_color=colour, line_width=1,
                            annotation_text=label,
                            annotation_position="right",
                            row=2, col=1,
                        )

                fig.update_layout(
                    height=600,
                    paper_bgcolor="#0d1117",
                    plot_bgcolor="#0d1117",
                    font=dict(color="#e6edf3", family="IBM Plex Mono, monospace"),
                    legend=dict(
                        bgcolor="#161b22",
                        bordercolor="#30363d",
                        borderwidth=1,
                    ),
                    xaxis_rangeslider_visible=False,
                    margin=dict(l=0, r=0, t=40, b=0),
                )
                fig.update_xaxes(gridcolor="#21262d", showgrid=True)
                fig.update_yaxes(gridcolor="#21262d", showgrid=True)

                st.plotly_chart(fig, use_container_width=True)

                # ── Current indicator values for selected ticker ───────────
                row = results[results["Ticker"] == selected_ticker].iloc[0]
                c1, c2, c3, c4, c5 = st.columns(5)
                c1.metric("RSI (14)",         f"{row['RSI (14)']:.1f}")
                c2.metric("% boven support",  f"{row['% boven support']:.2f}%")
                c3.metric("Vol ratio",        f"{row['Vol ratio']:.2f}×")
                c4.metric("Dag wijziging",    f"{row['Dag wijziging %']:+.2f}%")
                c5.metric("Support",          f"{row['Support']:.2f}")

else:
    # ── Landing state ─────────────────────────────────────────────────────────
    st.markdown("""
    <div style="
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 2.5rem 2rem;
        text-align: center;
        color: #8b949e;
        margin-top: 2rem;
    ">
        <div style="font-size:2.5rem;margin-bottom:0.5rem">🔎</div>
        <div style="font-size:1.1rem;color:#e6edf3;font-weight:600;margin-bottom:0.5rem">
            Alpha Scanner klaar voor gebruik
        </div>
        <div style="font-size:0.85rem">
            Selecteer beurzen links in de sidebar, pas eventueel de parameters aan,<br>
            en klik op <strong style="color:#58a6ff">▶ Start scan</strong>.
        </div>
        <div style="margin-top:1.5rem;display:flex;gap:1rem;justify-content:center;flex-wrap:wrap">
            <div style="background:#161b22;border:1px solid #30363d;border-radius:6px;padding:10px 18px;font-size:0.78rem">
                📌 RSI ≤ 45 (dip / oververkocht)
            </div>
            <div style="background:#161b22;border:1px solid #30363d;border-radius:6px;padding:10px 18px;font-size:0.78rem">
                📌 Koers 0–5 % boven support
            </div>
            <div style="background:#161b22;border:1px solid #30363d;border-radius:6px;padding:10px 18px;font-size:0.78rem">
                📌 Volume ≥ 0.8× 20d-gemiddelde
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
