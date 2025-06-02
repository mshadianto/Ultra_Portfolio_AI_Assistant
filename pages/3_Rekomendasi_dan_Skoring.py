# Ultra Portfolio AI - Halaman Rekomendasi & Skoring

import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Rekomendasi & Skoring", layout="wide")
st.title("🤖 Rekomendasi & Skoring")

st.markdown("""
Fitur ini memanfaatkan AI dan parameter pribadi Anda untuk:
- Menilai profil risiko
- Memberi saran alokasi aset
- Menampilkan strategi investasi yang cocok
- Memberikan peringatan risiko bila perlu
""")

# Profil risiko sederhana
st.subheader("🧠 Tes Profil Risiko")

usia = st.slider("Berapa usia Anda?", 18, 75, 30)
pengalaman = st.selectbox("Pengalaman Investasi:", ["Pemula", "Menengah", "Ahli"])
kebutuhan = st.selectbox("Tujuan utama investasi Anda:", ["Pertumbuhan aset jangka panjang", "Pendapatan pasif rutin", "Likuiditas jangka pendek"])
risk_tolerance = st.radio("Toleransi Risiko Anda:", ["Rendah", "Sedang", "Tinggi"])

# Skor risiko
skor = usia / 100
if pengalaman == "Menengah": skor += 0.1
if pengalaman == "Ahli": skor += 0.2
if kebutuhan == "Pendapatan pasif rutin": skor -= 0.1
if kebutuhan == "Likuiditas jangka pendek": skor -= 0.15
if risk_tolerance == "Tinggi": skor += 0.2
elif risk_tolerance == "Sedang": skor += 0.1

skor = min(max(skor, 0), 1)

st.metric("📊 Skor Profil Risiko Anda", f"{skor:.2f}")

# Rekomendasi Alokasi
st.subheader("🗂️ Rekomendasi Alokasi Aset")
if skor < 0.3:
    alokasi = {"Obligasi": 70, "Pasar Uang": 20, "Saham": 10}
elif skor < 0.6:
    alokasi = {"Obligasi": 40, "Pasar Uang": 20, "Saham": 40}
else:
    alokasi = {"Obligasi": 20, "Pasar Uang": 10, "Saham": 70}

df_alokasi = pd.DataFrame.from_dict(alokasi, orient='index', columns=["% Alokasi"])
st.bar_chart(df_alokasi)
st.dataframe(df_alokasi.T)

# Risiko & Catatan
st.subheader("⚠️ Catatan Risiko")
if skor < 0.3:
    st.warning("⚠️ Anda termasuk investor konservatif. Prioritaskan stabilitas dan hindari saham spekulatif.")
elif skor < 0.7:
    st.info("ℹ️ Anda tergolong moderat. Diversifikasi adalah kunci.")
else:
    st.success("🚀 Anda termasuk agresif. Potensi return tinggi, namun tetap waspada terhadap volatilitas.")