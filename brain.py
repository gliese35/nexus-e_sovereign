import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import datetime

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

@st.cache_resource
def get_strategic_engine():
    if not API_KEY: return None
    genai.configure(api_key=API_KEY)
    try:
        return genai.GenerativeModel("models/gemini-1.5-flash")
    except: return None

def generate_sovereign_strategy(delta, scenario, user_name):
    """
    Sovereign Intelligence: Kurumsal düzeyde CSS ve Finansal Mühendislik Raporu.
    """
    df = pd.read_csv("data/sales_data.csv")
    perf = df.groupby('Urun_Adi')['Net_Kar'].sum().sort_values(ascending=False)
    
    alpha = perf.index[0]
    omega = perf.index[-1]
    today_date = datetime.datetime.now().strftime("%d.%m.%Y")
    
    # DÜNYA STANDARTLARINDA KURUMSAL PROMPT
    prompt = f"""
    Sen NEXUS-E SOVEREIGN'in Baş Danışmanısın (McKinsey/BCG Seviyesi).
    
    KURUMSAL BİLGİLER:
    - Yönetici: {user_name}
    - Senaryo: {scenario}
    - Bütçe İnovasyonu: %{delta}
    - Lider Ürün: {alpha} | Riskli Ürün: {omega}
    
    GÖREV: Aşağıdaki şablonu kullanarak, e-ticaret ve KOBİ finansı odaklı 'Dahi' bir Yönetici Özeti (Executive Brief) oluştur. Dili son derece akademik, teknik (EBITDA, ROAS, LTV, Entropi) ve kurumsal olmalı.
    
    ŞABLON (Aynen bu yapıyı kullan):
    ======================================================
    NEXUS-E SOVEREIGN : STRATEJİK İCRA RAPORU
    ======================================================
    TARİH    : {today_date}
    LOKASYON : İzmir HQ
    YÖNETİCİ : {user_name} (Chief Strategy Officer)
    SENARYO  : {scenario} (Kaldıraç: %{delta})
    ======================================================
    
    [ 1. HESAPLAMALI SOSYAL BİLİMLER (CSS) PAZAR ANALİZİ ]
    (Buraya %{delta} değişiminin tüketici psikolojisi ve kolektif pazar davranışı üzerindeki etkisini yaz.)
    
    [ 2. E-TİCARET OPERASYONEL STRES TESTİ ]
    (Buraya '{alpha}' ve '{omega}' ürünlerinin stok devir hızı, ROAS maliyetleri ve lojistik risklerini yaz.)
    
    [ 3. KOBİ FİNANSAL LİKİDİTE PROJEKSİYONU ]
    (Buraya senaryoya göre nakit akışı, EBITDA marjı ve riskten korunma (hedging) stratejisini yaz.)
    
    [ 4. OTONOM İCRA TALİMATI (EXECUTIVE DIRECTIVE) ]
    (CEO için madde imli, sarsılmaz, net 2 adet finansal hamle yaz.)
    
    ======================================================
    """
    
    try:
        model = get_strategic_engine()
        response = model.generate_content(prompt)
        return response.text
    except:
        # KOTA DOLARSA ÇALIŞACAK KUSURSUZ TABLOLU FALLBACK
        return f"""
======================================================
NEXUS-E SOVEREIGN : OFFLINE STRATEJİ RAPORU
======================================================
TARİH    : {today_date}
LOKASYON : İzmir HQ
YÖNETİCİ : {user_name}
SENARYO  : {scenario} (Kaldıraç: %{delta})
======================================================

[ 1. HESAPLAMALI SOSYAL BİLİMLER (CSS) ANALİZİ ]
{scenario} etkisi altında pazar entropisi artmaktadır. %{delta} bütçe optimizasyonu, tüketici güven endeksini stabilize etmek için yeterli toleransa sahiptir.

[ 2. OPERASYONEL RİSK MATRİSİ ]
| Ürün Grubu | Statü | Aksiyon Planı |
|---|---|---|
| {alpha} | Lider (Alpha) | %20 Stok Artışı & ROAS Optimizasyonu |
| {omega} | Riskli (Omega) | Likiditeyi Durdur & Zarar Kes (Stop-Loss) |

[ 3. OTONOM İCRA TALİMATI ]
1. Sayın {user_name}, agresif büyüme stratejisi gereği '{alpha}' kanalına tüm pazarlama gücünü aktarın.
2. İşletme sermayesini (Working Capital) korumak adına yeni arge harcamalarını {scenario} sonrasına erteleyin.

======================================================
"""