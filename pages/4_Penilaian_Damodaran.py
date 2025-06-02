# Ultra Portfolio AI App - Penilaian Damodaran

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Penilaian Damodaran", layout="wide")
st.title("📋 Penilaian Damodaran")

st.markdown("""
Modul ini akan memuat:
- Penilaian menggunakan pendekatan DCF (Discounted Cash Flow)
- Margin of safety
- Simulasi pertumbuhan FCFF/FCFE
- Sensitivitas terhadap perubahan asumsi WACC dan terminal growth
- 📈 Analitik tambahan: perbandingan proyeksi & total nilai wajar pada beberapa skenario
""")

st.subheader("🧮 Simulasi FCFF")
wacc = st.number_input("Masukkan WACC (%)", min_value=0.0, max_value=100.0, value=10.0) / 100
growth_rate = st.number_input("Masukkan growth rate (%)", min_value=0.0, max_value=100.0, value=5.0) / 100
fcff = st.number_input("Masukkan FCFF saat ini (dalam juta)", value=1000.0)
years = st.slider("Horizon tahun proyeksi", 1, 10, 5)

original_fcff = fcff  # simpan untuk hitung terminal value nanti

fcff_series = []
pv_series = []
data = []
for i in range(1, years+1):
    fcff = fcff * (1 + growth_rate)
    discount_factor = (1 + wacc) ** i
    present_value = fcff / discount_factor
    data.append({"Tahun": f"Tahun {i}", "FCFF": fcff, "Present Value": present_value})
    fcff_series.append(fcff)
    pv_series.append(present_value)

df_fcff = pd.DataFrame(data)
st.dataframe(df_fcff.style.format({col: "{:.2f}" for col in df_fcff.select_dtypes(include=[np.number]).columns}), use_container_width=True)

npv = df_fcff["Present Value"].sum()
st.success(f"📌 Nilai sekarang FCFF (NPV): ${npv:,.2f} juta")

st.subheader("🏁 Terminal Value dan Margin of Safety")
terminal_value = fcff * (1 + growth_rate) / (wacc - growth_rate)
pv_terminal = terminal_value / ((1 + wacc) ** years)

st.write(f"💰 Terminal Value (TV): ${terminal_value:,.2f} juta")
st.write(f"📉 Present Value of TV: ${pv_terminal:,.2f} juta")

total_value = npv + pv_terminal
st.success(f"🔢 Total Nilai Wajar (DCF + TV): ${total_value:,.2f} juta")

market_price = st.number_input("Masukkan nilai pasar saat ini (dalam juta)", value=total_value)
margin_of_safety = (total_value - market_price) / total_value * 100
st.metric(label="🛡️ Margin of Safety", value=f"{margin_of_safety:.2f} %")

st.caption("Simulasi ini merupakan pendekatan sederhana untuk memahami valuasi berdasarkan DCF dengan terminal value dan margin of safety.")

# 🔄 Sensitivitas WACC dan Pertumbuhan
st.subheader("📊 Sensitivitas terhadap WACC & Pertumbuhan")
wacc_range = np.linspace(wacc - 0.03, wacc + 0.03, 7)
growth_range = np.linspace(growth_rate - 0.02, growth_rate + 0.02, 5)

sensitivity_matrix = pd.DataFrame(index=[f"{g*100:.1f}%" for g in growth_range], columns=[f"{w*100:.1f}%" for w in wacc_range])

for g in growth_range:
    for w in wacc_range:
        tv = fcff * (1 + g) / (w - g) if w > g else np.nan
        pv_tv = tv / ((1 + w) ** years) if not np.isnan(tv) else np.nan
        total_val = npv + pv_tv if not np.isnan(pv_tv) else np.nan
        sensitivity_matrix.loc[f"{g*100:.1f}%", f"{w*100:.1f}%"] = round(total_val, 2) if total_val else np.nan

st.write("### Matriks Sensitivitas Total Nilai Wajar")
st.dataframe(sensitivity_matrix)

fig, ax = plt.subplots()
sns.heatmap(sensitivity_matrix.astype(float), annot=True, fmt=".0f", cmap="YlGnBu", ax=ax)
plt.xlabel("WACC")
plt.ylabel("Growth Rate")
st.pyplot(fig)

# 📊 Tambahan: Visualisasi Proyeksi FCFF & PV
st.subheader("📈 Grafik Proyeksi FCFF dan Present Value")
fig2, ax2 = plt.subplots()
ax2.plot(range(1, years+1), fcff_series, marker='o', label='FCFF')
ax2.plot(range(1, years+1), pv_series, marker='x', label='Present Value')
ax2.set_title("Proyeksi FCFF dan PV")
ax2.set_xlabel("Tahun")
ax2.set_ylabel("Nilai (juta)")
ax2.legend()
st.pyplot(fig2)

st.caption("Grafik ini membantu memahami bagaimana pertumbuhan FCFF dibandingkan dengan nilai sekarangnya tiap tahun.")
