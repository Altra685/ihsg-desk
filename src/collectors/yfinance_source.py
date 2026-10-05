"""Daily price fetching from a public source (yfinance)."""
from __future__ import annotations

from typing import Sequence


def fetch_daily(ticker: str, period: str = "6mo"):
    """Fetch daily OHLCV. Returns a list of dicts."""
    import yfinance as yf

    df = yf.Ticker(ticker).history(period=period, interval="1d")
    rows: list[dict] = []
    for ts, r in df.iterrows():
        rows.append({
            "date": ts.date().isoformat(),
            "open": float(r["Open"]),
            "high": float(r["High"]),
            "low": float(r["Low"]),
            "close": float(r["Close"]),
            "volume": float(r["Volume"]),
        })
    return rows


def load_csv(path: str) -> list[dict]:
    """Read OHLCV from a CSV. Columns: date,open,high,low,close,volume."""
    import csv

    out: list[dict] = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out.append({
                "date": row["date"],
                "open": float(row["open"]),
                "high": float(row["high"]),
                "low": float(row["low"]),
                "close": float(row["close"]),
                "volume": float(row.get("volume") or 0),
            })
    return out