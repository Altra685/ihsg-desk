"""
IHSG Desk — versi publik.

Panel sederhana untuk menampilkan indikator teknikal dasar pada satu saham.
Versi ini hanya memuat indikator mentah (SMA, EMA, RSI, MACD, ATR, Bollinger).
Sistem penilaian, penyaring risiko, dan mesin sinyal tidak disertakan.
"""
from __future__ import annotations

import streamlit as st
import pandas as pd

from src.indicators import analyze

st.set_page_config(page_title="IHSG Desk", layout="wide")
st.title("IHSG Desk")
st.caption("Indikator teknikal dasar — versi publik")

ticker = st.text_input("Kode saham", value="BBCA.JK")
periode = st.selectbox("Periode data", ["3mo", "6mo", "1y"], index=1)

if st.button("Muat data"):
    try:
        from src.collectors.yfinance_source import fetch_daily
        rows = fetch_daily(ticker, periode)
        hasil = analyze(rows)
        if not hasil.get("ok"):
            st.warning(f"Data tidak cukup: {hasil.get('reason')}")
        else:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Harga terakhir", f"{hasil['last_close']:.2f}")
            c2.metric("SMA-20", f"{hasil.get('sma20') or 0:.2f}")
            c3.metric("RSI-14", f"{hasil.get('rsi14') or 0:.1f}")
            c4.metric("Tren", hasil.get("trend", "-"))
            macd = hasil.get("macd") or {}
            st.write({
                "MACD": macd.get("macd"),
                "Signal": macd.get("signal"),
                "Histogram": macd.get("hist"),
                "ATR-14": hasil.get("atr14"),
                "Bollinger": hasil.get("bollinger"),
            })
            df = pd.DataFrame(rows)
            df["date"] = pd.to_datetime(df["date"])
            st.line_chart(df.set_index("date")["close"])
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")

st.divider()
st.caption("Versi publik ini hanya memuat indikator teknikal. "
           "Komponen penilaian dan manajemen risiko tidak disertakan.")
