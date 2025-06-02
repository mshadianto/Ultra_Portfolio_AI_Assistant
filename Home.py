# Ultra Portfolio AI App - Home

import streamlit as st
from datetime import date
from PIL import Image
import base64

st.set_page_config(
    page_title="Ultra Portfolio AI Assistant",
    page_icon="💼",
    layout="wide"
)

def show_logo(path):
    logo = Image.open(path)
    st.markdown(
        f"""
        <div style="text-align: center; margin-top: 2rem; animation: fadeIn 2s ease-out;">
            <img src="data:image/png;base64,{base64.b64encode(open(path, "rb").read()).decode()}" width="180"/>
        </div>
        """,
        unsafe_allow_html=True
    )

show_logo("logo MSH.png")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Space Grotesk', sans-serif;
            background-color: #f9f9f9;
            color: #1c1c1c;
        }

        .big-title {
            font-size: 3.2em;
            font-weight: 700;
            color: #003366;
            animation: fadeInDown 1.2s ease-out;
        }

        .subtitle {
            font-size: 1.3em;
            color: #006699;
            margin-top: -10px;
            animation: fadeInUp 1.2s ease-out;
        }

        .highlight {
            background: linear-gradient(135deg, #e6f2ff, #ffffff);
            padding: 1.2rem;
            border-left: 6px solid #3399cc;
            border-radius: 0.6rem;
            font-size: 1.05em;
            animation: slideIn 1s ease-in-out;
        }

        .card {
            background-color: #ffffff;
            padding: 1.2rem;
            margin-bottom: 1rem;
            border-left: 6px solid #ff9933;
            border-radius: 0.5rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }

        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }

        @keyframes fadeIn {
            from {opacity: 0; transform: scale(0.9);}
            to {opacity: 1; transform: scale(1);}
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="big-title">💼 Ultra Portfolio AI Assistant</div>
<div class="subtitle">Optimalisasi strategi investasi dengan AI, rebalancing, benchmarking, dan proyeksi finansial.</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="highlight">
📌 **Navigasi fitur lengkap**:<br>
✅ Simulasi dan manajemen risiko<br>
✅ Kalkulator tujuan finansial<br>
✅ Rekomendasi AI & penilaian skor<br>
✅ Penilaian saham berbasis DCF<br>
✅ Matriks risiko Damodaran<br>
✅ Benchmarking saham global & sektoral
</div>
""", unsafe_allow_html=True)

with st.expander("📖 Tentang Aplikasi"):
    st.markdown("""
    Aplikasi ini dikembangkan untuk membantu investor ritel maupun analis profesional dalam mengevaluasi dan mengoptimalkan portofolio saham mereka.
    Didukung oleh model analitik modern, data real-time, dan integrasi AI.
    """)

with st.expander("🚀 Tips Menggunakan"):
    st.markdown("""
    - Masukkan minimal 2 ticker saham (mis. `BBCA.JK, BBRI.JK`)
    - Ubah rentang tanggal untuk simulasi historis
    - Gunakan fitur skoring untuk membandingkan performa
    - Simpan preset alokasi jika diperlukan
    """)

st.markdown("""
---
<div style="font-size: 0.9em; color: gray;">
⚠️ **Disclaimer:** Aplikasi ini bersifat edukatif. Semua output berbasis simulasi dan AI, bukan saran investasi. Investor tetap bertanggung jawab atas keputusan masing-masing.
</div>
""", unsafe_allow_html=True)

st.caption("🧠 Dibuat oleh MS Hadianto | Versi: Beta {}".format(date.today().isoformat()))
