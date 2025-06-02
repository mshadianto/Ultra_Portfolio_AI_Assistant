# Ultra Portfolio AI App - Damodaran Risk Matrix

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Damodaran Risk Matrix", layout="wide")
st.title("📉 Damodaran Risk Matrix")

st.markdown("""
Modul ini memungkinkan Anda:
- Menghitung beta saham terhadap indeks pasar
- Membandingkan beta saham dengan beta industri
- Menampilkan visualisasi risiko berbasis leverage dan beta
- Referensi screener untuk eksplorasi saham risiko tinggi/rendah
""")

st.subheader("🧠 Hitung Beta Saham terhadap Pasar")
ticker = st.text_input("Masukkan ticker saham (misal: BBCA.JK)", "BBCA.JK")
market_index = st.text_input("Masukkan ticker indeks pasar (misal: ^JKSE)", "^JKSE")
industry_beta = st.number_input("Masukkan rata-rata beta industri (opsional)", value=1.0)
start_date = st.date_input("Tanggal awal", pd.to_datetime("2022-01-01"))
end_date = st.date_input("Tanggal akhir", pd.to_datetime("2023-01-01"))

@st.cache_data
def calculate_beta(stock_ticker, market_ticker, start, end):
    df_stock = yf.download(stock_ticker, start=start, end=end)
    df_market = yf.download(market_ticker, start=start, end=end)

    if 'Adj Close' not in df_stock.columns or 'Adj Close' not in df_market.columns:
        return None

    returns_stock = df_stock['Adj Close'].pct_change().dropna()
    returns_market = df_market['Adj Close'].pct_change().dropna()

    combined = pd.concat([returns_stock, returns_market], axis=1).dropna()
    if combined.shape[0] < 30:
        return None

    X = combined.iloc[:, 1].values.reshape(-1, 1)
    y = combined.iloc[:, 0].values
    model = LinearRegression().fit(X, y)
    return model.coef_[0]

if ticker and market_index:
    beta_val = calculate_beta(ticker, market_index, start_date, end_date)
    if beta_val is not None:
        st.success(f"📊 Beta saham {ticker} terhadap {market_index}: {beta_val:.4f}")
        if industry_beta:
            gap = beta_val - industry_beta
            st.info(f"Perbandingan dengan rata-rata industri: {gap:+.2f}")
    else:
        st.warning("Data historis tidak cukup atau tidak tersedia untuk menghitung beta.")

st.markdown("""
#### 📌 Referensi Screener Saham:
- [Yahoo Finance Screener](https://finance.yahoo.com/screener/)
- [TradingView Screener](https://www.tradingview.com/screener/)
- [Finviz](https://finviz.com/screener.ashx) (untuk saham US)
Gunakan screener ini untuk mencari saham dengan karakteristik beta, PER, PBV, dan margin sesuai strategi valuasi.
""")
