# Ultra Portfolio AI App - Optimized with Lazy Tabs and Efficient Memory

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from scipy.optimize import minimize

st.set_page_config(page_title="Simulasi dan Risiko", layout="wide")
st.title("📈 Simulasi & Risiko")

st.markdown("""
Fitur ini memungkinkan Anda untuk:
- Melihat harga historis saham
- Analisis korelasi antar saham
- Simulasi rebalancing portofolio
- Alokasi aset optimal berbasis model Markowitz
""")

# Input ticker
tickers = st.text_input("Masukkan ticker saham (pisah dengan koma)", "BBRI.JK,BMRI.JK").upper().split(',')
start_date = st.date_input("Tanggal mulai", pd.to_datetime("2019-01-01"))
end_date = st.date_input("Tanggal akhir", pd.to_datetime("today"))

@st.cache_data
def fetch_data(tickers, start, end):
    df = yf.download(tickers, start=start, end=end, group_by='ticker', auto_adjust=True)
    if len(tickers) == 1:
        return pd.DataFrame({tickers[0]: df['Close']})
    else:
        close_prices = pd.DataFrame()
        for ticker in tickers:
            try:
                close_prices[ticker] = df[ticker]['Close']
            except:
                pass
        return close_prices.dropna(axis=1, how='all')

data = fetch_data(tickers, start_date, end_date)

if data.empty:
    st.warning("Tidak ada data yang tersedia. Periksa kembali ticker dan tanggal.")
else:
    st.success("✅ Data berhasil diambil!")
    fig = px.line(data, title="📈 Harga Saham Historis")
    fig.update_layout(xaxis_title="Tanggal", yaxis_title="Harga", legend_title="Ticker")
    st.plotly_chart(fig, use_container_width=True)

    # Simulasi Rebalancing
    st.subheader("🔁 Simulasi Rebalancing Portofolio")
    if len(data.columns) >= 2:
        returns = data.pct_change().dropna()

        st.markdown("### 🎚️ Sesuaikan Bobot Manual (Slider)")
        manual_weights = []
        for ticker in data.columns:
            manual_weights.append(
                st.slider(f"{ticker}", 0.0, 1.0, 1.0 / len(data.columns), step=0.01)
            )
        sum_weights = sum(manual_weights)
        if sum_weights == 0:
            weights = np.repeat(1/returns.shape[1], returns.shape[1])
        else:
            weights = np.array(manual_weights) / sum_weights

        initial_value = 10000
        rebalance_value = [initial_value]

        for i in range(1, len(returns)):
            daily_returns = (returns.iloc[i].values + 1)
            portfolio_value = rebalance_value[-1] * np.dot(daily_returns, weights)
            rebalance_value.append(portfolio_value)

        port_series = pd.Series(rebalance_value, index=returns.index)
        st.line_chart(port_series.rename("Portofolio Value"))

    # Alokasi Optimal (Markowitz)
    st.subheader("📌 Alokasi Aset Optimal (Model Markowitz)")
    if len(data.columns) >= 2:
        returns = data.pct_change().dropna()
        mean_returns = returns.mean() * 252
        cov_matrix = returns.cov() * 252

        def neg_sharpe(weights, mean_returns, cov_matrix, risk_free_rate=0.03):
            weights = np.array(weights)
            ret = np.dot(weights, mean_returns)
            vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            return -(ret - risk_free_rate) / vol

        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for _ in range(len(data.columns)))
        initial = len(data.columns) * [1. / len(data.columns)]

        result = minimize(neg_sharpe, initial, args=(mean_returns, cov_matrix), method='SLSQP', bounds=bounds, constraints=constraints)

        if result.success:
            opt_weights = result.x
            df_alloc = pd.DataFrame({"Ticker": data.columns, "Bobot Optimal": opt_weights})
            st.dataframe(df_alloc.style.format({"Bobot Optimal": "{:.2%}"}), use_container_width=True)
        else:
            st.error("Gagal menghitung alokasi optimal.")
