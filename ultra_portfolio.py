# Ultra Portfolio AI App - Optimized with Lazy Tabs and Efficient Memory

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from openai import OpenAI

st.set_page_config(page_title="💹 Ultra Portfolio AI", layout="wide")
st.title("💼 Ultra Portfolio AI Assistant")

st.markdown("🔍 **Selamat datang!** Aplikasi ini membantu Anda mensimulasikan, memahami, dan mengoptimalkan strategi investasi secara otomatis menggunakan AI.")
st.info("💡 Fitur: simulasi historis, rebalancing, kalkulator tujuan, rekomendasi AI, dan skor portofolio.")

with st.sidebar:
    st.header("🤖 AI Chat Assistant")
    openai_api_key = st.text_input("🔐 OpenAI API Key", type="password")
    chat_input = st.text_area("Tanya tentang investasi kamu...")
    if st.button("💬 Tanya AI") and openai_api_key and chat_input:
        client = OpenAI(api_key=openai_api_key)
        with st.spinner("🧠 Meminta jawaban dari AI..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": chat_input}]
            )
        ai_msg = response.choices[0].message.content
        st.success(ai_msg)
        if any(x in ai_msg.lower() for x in ["risiko tinggi", "waspada", "volatil"]):
            st.warning("⚠️ AI memberikan peringatan risiko. Evaluasi keputusan Anda secara hati-hati.")

    st.markdown("---")
    st.markdown("👤 **Dibuat oleh:** [MS Hadianto](https://www.linkedin.com/in/ms-hadianto)", unsafe_allow_html=True)

# Tabs
main_tab = st.selectbox("🧭 Pilih Analisis:", ["📊 Simulasi & Risiko", "🎯 Tujuan Finansial", "🧠 Rekomendasi & Skoring"])

if main_tab == "📊 Simulasi & Risiko":
    st.subheader("📈 Pilih Saham dan Waktu")
    tickers_input = st.text_input("Masukkan simbol saham (pisah dengan koma)", "AAPL,MSFT,GOOG")
    tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    start = st.date_input("Mulai", pd.to_datetime("2014-01-01"))
    end = st.date_input("Sampai", pd.to_datetime("2024-01-01"))

    @st.cache_data
    def get_data(tickers, start, end):
        return yf.download(tickers, start=start, end=end)["Close"]

    try:
        data = get_data(tickers, start, end)
    except Exception as e:
        st.error(f"Gagal mengambil data: {e}")
        data = pd.DataFrame()

    if not data.empty:
        cleaned_data = data.dropna()
        if not cleaned_data.empty:
            fig = px.line(cleaned_data, title="📈 Harga Saham Historis")
            fig.update_layout(legend_title="Saham", xaxis_title="Tanggal", yaxis_title="Harga")
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("📊 Heatmap Risiko")
        st.markdown("""
        <small>Heatmap ini menunjukkan korelasi antara saham-saham yang dipilih.
        Korelasi tinggi (warna kuning) berarti pergerakan harga sangat mirip — tidak ideal untuk diversifikasi.
        Korelasi rendah (warna ungu/gelap) lebih baik untuk mengurangi risiko portofolio.</small>
        """, unsafe_allow_html=True)
        returns = data.pct_change(fill_method=None).dropna()
        corr = returns.corr()
        fig = go.Figure(data=go.Heatmap(z=corr.values, x=corr.columns, y=corr.columns, colorscale="Viridis"))
        st.plotly_chart(fig)

        st.subheader("⏳ Perbandingan Horizon Investasi")
        horizons = [1, 3, 5, 10]
        initial = 10000
        annual_return = returns.mean() * 252
        comparison = {"Horizon (Tahun)": [], "Estimasi Akhir (USD)": [], "CAGR (%)": []}

        for h in horizons:
            r = annual_return.mean()
            end_value = initial * ((1 + r) ** h)
            cagr = ((end_value / initial) ** (1/h)) - 1
            comparison["Horizon (Tahun)"].append(h)
            comparison["Estimasi Akhir (USD)"].append(round(end_value, 2))
            comparison["CAGR (%)"].append(round(cagr * 100, 2))

        df_horizon = pd.DataFrame(comparison)
        st.dataframe(df_horizon, use_container_width=True)
        st.caption("Simulasi pertumbuhan dana jika diinvestasikan dalam saham yang dipilih selama periode tertentu.")

        st.subheader("🔁 Simulasi Rebalancing Tahunan")
        st.caption("📘 Strategi: 60% Saham, 40% Instrumen Lain. Rebalance setiap akhir tahun.")

        st.markdown("### ℹ️ Apa itu Instrumen Pendapatan Tetap atau Alternatif?")
        pendapatan_tetap_jenis = st.selectbox("Pilih jenis instrumen pendapatan tetap/alternatif:", [
            "Obligasi Negara (SBN)",
            "Reksa Dana Pendapatan Tetap",
            "Deposito",
            "Pasar Uang",
            "Logam Mulia",
            "Properti Virtual (REITs)",
            "Simulasi Flat 7% Return"
        ])

        instrumen_return = {
            "Obligasi Negara (SBN)": 0.065,
            "Reksa Dana Pendapatan Tetap": 0.055,
            "Deposito": 0.04,
            "Pasar Uang": 0.035,
            "Logam Mulia": 0.09,
            "Properti Virtual (REITs)": 0.08,
            "Simulasi Flat 7% Return": 0.07,
        }

        bond_return = instrumen_return.get(pendapatan_tetap_jenis, 0.05)
        st.info(f"""
Instrumen {pendapatan_tetap_jenis} menargetkan return tahunan sekitar {bond_return*100:.2f}%. Cocok untuk profil risiko konservatif hingga moderat.
""")

        equity = data[tickers[0]].dropna()
        df_rebal = pd.DataFrame({"Equity": equity})
        df_rebal["Instrument"] = 10000 * ((1 + bond_return) ** ((df_rebal.index - df_rebal.index[0]).days / 365))

        port_values = []
        weight_eq = 0.6
        weight_bd = 0.4
        units_eq = 6000 / df_rebal.iloc[0]["Equity"]
        units_bd = 4000 / df_rebal.iloc[0]["Instrument"]

        for i, row in df_rebal.iterrows():
            total = units_eq * row["Equity"] + units_bd * row["Instrument"]
            if i.month == 12 and i.day == 31:
                units_eq = (total * weight_eq) / row["Equity"]
                units_bd = (total * weight_bd) / row["Instrument"]
            port_values.append(total)

        df_rebal["Total Value"] = port_values
        fig_rebal = px.line(df_rebal, y="Total Value", title="📈 Pertumbuhan Portofolio dengan Rebalancing")
        fig_rebal.update_layout(xaxis_title="Tanggal", yaxis_title="Total Value", template="plotly_white")
        st.plotly_chart(fig_rebal, use_container_width=True)
    else:
        st.warning("Data harga saham tidak tersedia. Periksa simbol dan koneksi.")
