# IHSG Desk

A small dashboard for displaying technical indicators on IDX stocks.

## Indicators

SMA, EMA, RSI, MACD, ATR, Bollinger Bands, and volume ratio — computed from the
closing price series.

## Running

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
streamlit run app.py
```

Enter a ticker (for example `BBCA.JK`), pick a period, then press **Load data**.

## Data source

Daily prices are fetched from a public source through `yfinance`. To use your
own file, call `src/collectors/yfinance_source.py::load_csv` with the columns
`date,open,high,low,close,volume`.

## Structure

```
app.py                     Streamlit application
src/indicators/            technical indicators
src/collectors/            data fetching
src/storage/schema.sql     base database schema
```

## License

MIT.