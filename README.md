# IHSG Desk

Panel sederhana untuk menampilkan indikator teknikal pada saham IDX.

Repositori ini memuat indikator mentah dan kerangka penyimpanan data. Sistem
penilaian, penyaring risiko, dan mesin sinyal yang dipakai pada aplikasi penuh
tidak disertakan.

## Indikator

SMA, EMA, RSI, MACD, ATR, Bollinger, dan rasio volume — dihitung dari deret
harga penutupan.

## Menjalankan

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
streamlit run app.py
```

Masukkan kode saham (misalnya `BBCA.JK`), pilih periode, lalu tekan **Muat data**.

## Sumber data

Harga harian diambil dari sumber publik melalui `yfinance`. Untuk data dari
berkas sendiri, gunakan `src/collectors/yfinance_source.py::load_csv` dengan
kolom `date,open,high,low,close,volume`.

## Struktur

```
app.py                     aplikasi Streamlit
src/indicators/            indikator teknikal
src/collectors/            pengambil data
src/storage/schema.sql     skema basis data dasar
```

## Catatan

Versi ini hanya menampilkan indikator. Versi lengkap menambahkan penilaian,
penyaringan risiko, dan pencatatan sinyal.

## Lisensi

MIT.