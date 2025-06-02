# Ultra Portfolio AI App - Peer Benchmarking

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf

st.set_page_config(page_title="Peer Benchmarking", layout="wide")
st.title("📊 Peer Benchmarking Saham")

st.markdown("""
Modul ini memungkinkan Anda:
- Membandingkan performa beberapa saham secara bersamaan
- Menganalisis korelasi dan volatilitas
- Visualisasi heatmap dan grafik pertumbuhan
- Skoring saham berdasarkan rasio Sharpe sederhana
- Filtering berdasarkan sektor
- Highlight saham terbaik
""")

st.subheader("📌 Input Saham")
tickers = st.text_input("Masukkan ticker saham (pisahkan dengan koma)", "BBCA.JK, BBRI.JK, BMRI.JK")
tickers_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]

start_date = st.date_input("Tanggal awal", pd.to_datetime("2023-01-01"))
end_date = st.date_input("Tanggal akhir", pd.to_datetime("2024-01-01"))

# Optional sector mapping (manual input or extended in production)
sector_map = {
    "BBCA.JK": "Perbankan",
    "BBRI.JK": "Perbankan",
    "BMRI.JK": "Perbankan",
    "TLKM.JK": "Telekomunikasi",
    "ASII.JK": "Otomotif",
    "INDF.JK": "Konsumsi"
}

selected_sector = st.selectbox("Filter sektor (opsional)", ["Semua"] + sorted(set(sector_map.values())))

@st.cache_data
def fetch_benchmark_data(tickers_list, start, end):
    try:
        df = yf.download(tickers_list, start=start, end=end, group_by="ticker", auto_adjust=True, progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            price_data = pd.DataFrame()
            for ticker in tickers_list:
                if (ticker, 'Close') in df.columns:
                    price_data[ticker] = df[(ticker, 'Close')]
            return price_data.dropna(axis=1, how='all')
        else:
            return df[["Close"]].rename(columns={"Close": tickers_list[0]}) if "Close" in df.columns else pd.DataFrame()
    except Exception as e:
        st.error(f"Gagal mengambil data: {e}")
        return pd.DataFrame()

if tickers_list:
    if selected_sector != "Semua":
        tickers_list = [t for t in tickers_list if sector_map.get(t, None) == selected_sector]

    with st.spinner("📡 Mengambil data saham..."):
        data = fetch_benchmark_data(tickers_list, start_date, end_date)

    if data.empty:
        st.warning("Data kosong. Periksa ticker dan tanggal.")
    else:
        st.subheader("📈 Grafik Harga Saham")
        st.line_chart(data)

        st.subheader("📉 Korelasi Return Harian")
        daily_returns = data.pct_change().dropna()
        corr = daily_returns.corr()
        fig, ax = plt.subplots()
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

        st.subheader("📊 Statistik Return")
        stats = daily_returns.describe().T[["mean", "std"]]
        stats.columns = ["Rata-rata Harian", "Volatilitas"]

        stats["Rasio Sharpe Kasar"] = stats["Rata-rata Harian"] / stats["Volatilitas"]
        stats["Skor"] = stats["Rasio Sharpe Kasar"].rank(ascending=False)

        best = stats["Skor"].idxmin()
        st.success(f"📈 Saham dengan skor tertinggi: {best} (Skor: {stats.loc[best, 'Skor']:.2f})")

        st.dataframe(stats.style.format({
            "Rata-rata Harian": "{:.2%}",
            "Volatilitas": "{:.2%}",
            "Rasio Sharpe Kasar": "{:.2f}",
            "Skor": "{:.2f}"
        }), use_container_width=True)

        st.caption("Rasio Sharpe kasar dihitung tanpa memperhitungkan risk-free rate untuk perbandingan antar saham secara cepat.")
