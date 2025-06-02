# 2_Tujuan_Finansial.py - Modul Tujuan Keuangan Masa Depan

import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Tujuan Finansial", layout="wide")
st.title("🎯 Tujuan Finansial")

st.markdown("""
Rancang kebutuhan dana masa depan seperti:
- Dana pensiun
- Biaya pendidikan anak
- Pembelian aset jangka panjang

Sistem akan menghitung:
- Nilai akhir yang dibutuhkan
- Kekurangan dana
- Kontribusi rutin yang dibutuhkan untuk mencapainya
""")

# Input Tujuan Finansial
col1, col2 = st.columns(2)

with col1:
    tujuan = st.selectbox("Pilih tujuan keuangan:", ["Pensiun", "Pendidikan Anak", "Pembelian Rumah", "Lainnya"])
    target_tahun = st.number_input("Berapa tahun lagi?", min_value=1, value=10)
    target_dana = st.number_input("Target dana yang dibutuhkan (Rp):", min_value=0, value=100000000)

with col2:
    saldo_sekarang = st.number_input("Saldo saat ini (Rp):", min_value=0, value=20000000)
    return_investasi = st.slider("Estimasi imbal hasil tahunan (%)", 0.0, 20.0, 8.0) / 100
    kontribusi_rutin = st.number_input("Kontribusi bulanan saat ini (Rp):", min_value=0, value=200000)

# Perhitungan
future_value_saldo = saldo_sekarang * ((1 + return_investasi) ** target_tahun)
future_value_kontribusi = kontribusi_rutin * (((1 + return_investasi/12) ** (target_tahun*12) - 1) / (return_investasi/12))
total_future = future_value_saldo + future_value_kontribusi

st.subheader("📊 Hasil Proyeksi")
col3, col4 = st.columns(2)

with col3:
    st.metric("Total Proyeksi Dana", f"Rp {total_future:,.0f}")
    st.metric("Selisih dari Target", f"Rp {total_future - target_dana:,.0f}", delta_color="inverse")

with col4:
    kebutuhan_bulanan = (target_dana - future_value_saldo) * (return_investasi/12) / (((1 + return_investasi/12) ** (target_tahun*12)) - 1)
    if kebutuhan_bulanan < 0:
        kebutuhan_bulanan = 0
    st.metric("Kontribusi Bulanan Disarankan", f"Rp {kebutuhan_bulanan:,.0f}")

# Visualisasi
st.subheader("📈 Visualisasi Akumulasi Dana")
proyeksi = []
for bulan in range(target_tahun * 12 + 1):
    nilai = saldo_sekarang * ((1 + return_investasi/12) ** bulan) + kontribusi_rutin * (((1 + return_investasi/12) ** bulan - 1) / (return_investasi/12))
    proyeksi.append(nilai)

df_proj = pd.DataFrame({"Bulan": list(range(len(proyeksi))), "Proyeksi Dana": proyeksi})
st.line_chart(df_proj.set_index("Bulan"))
