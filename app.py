"""
IHSG Desk.

A small dashboard for displaying basic technical indicators on a single stock
(SMA, EMA, RSI, MACD, ATR, Bollinger).
"""
from __future__ import annotations

import streamlit as st
import pandas as pd

from src.indicators import analyze

st.set_page_config(page_title="IHSG Desk", layout="wide")
st.title("IHSG Desk")
st.caption("Daily technical indicators")

ticker = st.text_input("Ticker", value="BBCA.JK")
period = st.selectbox("Data period", ["3mo", "6mo", "1y"], index=1)

if st.button("Load data"):
    try:
        from src.collectors.yfinance_source import fetch_daily
        rows = fetch_daily(ticker, period)
        result = analyze(rows)
        if not result.get("ok"):
            st.warning(f"Insufficient data: {result.get('reason')}")
        else:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Last price", f"{result['last_close']:.2f}")
            c2.metric("SMA-20", f"{result.get('sma20') or 0:.2f}")
            c3.metric("RSI-14", f"{result.get('rsi14') or 0:.1f}")
            c4.metric("Trend", result.get("trend", "-"))
            macd = result.get("macd") or {}
            st.write({
                "MACD": macd.get("macd"),
                "Signal": macd.get("signal"),
                "Histogram": macd.get("hist"),
                "ATR-14": result.get("atr14"),
                "Bollinger": result.get("bollinger"),
            })
            df = pd.DataFrame(rows)
            df["date"] = pd.to_datetime(df["date"])
            st.line_chart(df.set_index("date")["close"])
    except Exception as e:
        st.error(f"Failed to load data: {e}")