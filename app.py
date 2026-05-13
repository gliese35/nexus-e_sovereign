import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import json
import time
import base64
from brain import generate_sovereign_strategy

st.set_page_config(page_title="NEXUS-E SOVEREIGN", page_icon="💎", layout="wide")

# --- UI TASARIMI: PRISM LIGHT EXECUTIVE ---
def load_prism_ui():
    st.markdown("""
        <style>
        .stApp { background: #ffffff; color: #1e293b; }
        h1, h2, h3, p, label, span { color: #0f172a !important; font-weight: 700 !important; }
        section[data-testid="stSidebar"] { background-color: #f8fafc !important; border-right: 1px solid #e2e8f0; }

        .ai-report-card {
            background: #ffffff; border-left: 12px solid #2563eb;
            padding: 35px; border-radius: 15px; border: 1px solid #e2e8f0;
            box-shadow: 0 10px 40px rgba(0,0,0,0.05); color: #1e293b !important;
            line-height: 1.6; font-size: 1.1rem; white-space: pre-wrap; font-family: 'Courier New', Courier, monospace;
        }

        div[data-testid="stMetricValue"] > div { color: #2563eb !important; font-weight: 900 !important; }
        .stButton>button {
            background: #2563eb !important; color: white !important;
            border-radius: 10px; font-weight: 800; border: none; height: 3rem; width: 100%;
        }
        </style>
        """, unsafe_allow_html=True)

USER_DB = "data/users.json"
def sync_db():
    try:
        with open(USER_DB, "r") as f: return json.load(f)
    except: return {}

if "user" not in st.session_state: st.session_state.user = None

if st.session_state.user is None:
    load_prism_ui()
    _, col, _ = st.columns([1, 1.8, 1])
    with col:
        st.markdown("<h1 style='text-align: center; color: #2563eb;'>🛡️ NEXUS-E SOVEREIGN</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["🔑 GİRİŞ", "📝 KAYIT"])
        with t2:
            with st.form("reg"):
                n = st.text_input("Ad Soyad", placeholder="Örn: Furkan Karaman")
                u = st.text_input("Kullanıcı")
                p = st.text_input("Şifre", type="password")
                if st.form_submit_button("HESABI AKTİF ET"):
                    db = sync_db(); db[u] = {"p": p, "n": n}
                    with open(USER_DB, "w") as f: json.dump(db, f, indent=4)
                    st.success("Sovereign Identity Tanımlandı!")
        with t1:
            with st.form("login"):
                lu = st.text_input("Kullanıcı"); lp = st.text_input("Şifre", type="password")
                if st.form_submit_button("BAĞLAN"):
                    db = sync_db()
                    if lu in db and db[lu]["p"] == lp:
                        st.session_state.user = db[lu]; st.rerun()
                    else: st.error("Erişim Reddedildi.")

else:
    u = st.session_state.user; load_prism_ui()

    with st.sidebar:
        st.markdown(f"<div style='text-align:center;'><h1>🛡️</h1><h3>{u['n']}</h3><p>Chief Strategy Officer</p></div>", unsafe_allow_html=True)
        st.write("---")
        st.subheader("⚙️ Sistem Analizi")
        st.success("✅ Neural Engine: Online")
        st.info("📍 Merkez: İzmir")
        
        st.write("---")
        st.subheader("📥 İndirme Merkezi")
        if "final_report" in st.session_state:
            # Word Dosyası İçin Kusursuz Kodlama
            b64 = base64.b64encode(st.session_state.final_report.encode('utf-8')).decode('utf-8')
            href = f'<a href="data:application/msword;base64,{b64}" download="Nexus_Strateji_Raporu.doc" style="text-decoration:none; color:white; background:#2563eb; padding:12px; border-radius:8px; display:block; text-align:center; font-weight:bold;">📥 PROFESYONEL RAPORU İNDİR (.DOC)</a>'
            st.markdown(href, unsafe_allow_html=True)
            st.caption("Rapor kurumsal mizanpaja uygundur.")
        else:
            st.caption("Rapor için analizi başlatın.")
            
        st.write("---")
        if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.user = None; st.rerun()

    st.markdown("<h1 style='text-align: center;'>🚀 OMNISCIENCE COMMAND CENTER</h1>", unsafe_allow_html=True)
    st.write("---")

    if os.path.exists("data/sales_data.csv"):
        df = pd.read_csv("data/sales_data.csv")
        
        st.subheader("🔮 Stratejik Senaryo Simülatörü")
        col_s1, col_s2 = st.columns([1, 1])
        scen = col_s1.selectbox("Pazar Senaryosu", ["Normal Pazar Şartları", "Rakiplerle Fiyat Savaşı", "Tedarik Zinciri Krizi"])
        val = col_s2.slider("Bütçe Kaldıraç Oranı (%)", -100, 100, 0)
        
        # 🚀 GRAFİĞİ DANS ETTİREN SİHİRLİ KOD (Diferansiyel Büyüme)
        df_sim = df.groupby('Urun_Adi')['Net_Kar'].sum().reset_index()
        
        if scen == "Rakiplerle Fiyat Savaşı":
            # Ucuzlar uçar, pahalılar düşer
            weights = np.linspace(1.8, 0.2, len(df_sim))
        elif scen == "Tedarik Zinciri Krizi":
            # Karışık, kaotik bir etki
            np.random.seed(42)
            weights = np.random.uniform(0.5, 1.5, len(df_sim))
        else:
            # Liderler daha da büyür
            weights = np.linspace(0.8, 1.5, len(df_sim))
            
        df_sim['Net_Kar'] = df_sim['Net_Kar'] * (1 + (val / 100) * weights)
        df_sim = df_sim.sort_values(by='Net_Kar', ascending=True) # Sıralamanın canlı değişmesini sağlar!

        c1, c2, c3 = st.columns(3)
        c1.metric("ÖNGÖRÜLEN CİRO", f"{df['Satis_Fiyati'].sum() * (1 + (val/100)):,.0f} ₺", f"{val}%")
        c2.metric("PROJEKTE KAR", f"{df_sim['Net_Kar'].sum():,.0f} ₺", f"{val}%")
        safe_name = u['n'].split()[0] if u['n'] and u['n'].split() else "Strategist"
        c3.metric("EXECUTOR", safe_name)

        st.write("---")
        st.subheader(f"📊 Diferansiyel Pazar Matrisi (Sıralama Anlık Değişir)")
        fig = px.bar(df_sim, x='Net_Kar', y='Urun_Adi', orientation='h', color='Net_Kar', color_continuous_scale='Blues')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#0f172a"))
        st.plotly_chart(fig, use_container_width=True)

        st.write("---")
        st.subheader("🧠 VIP AI Strategy Intelligence")
        
        if st.button("🔍 OTONOM ANALİZİ VE KURUMSAL RAPORU BAŞLAT"):
            with st.status("🧠 Sovereign Engine Derin Analiz Yapıyor...", expanded=True) as status:
                st.write("📈 CSS entropi verileri süzülüyor...")
                time.sleep(1.5)
                st.write(f"🎯 KOBİ nakit akış senaryosu ({scen}) hesaplanıyor...")
                report_text = generate_sovereign_strategy(val, scen, u['n'])
                st.session_state.final_report = report_text
                status.update(label="✅ Analiz ve Rapor Tamamlandı!", state="complete", expanded=False)
            
            # Ekranda Raporu Gösterme (Kutu İçinde, Kurumsal Font)
            st.markdown(f"<div class='ai-report-card'>{report_text}</div>", unsafe_allow_html=True)
    else:
        st.error("Veri dosyası (CSV) bulunamadı!")