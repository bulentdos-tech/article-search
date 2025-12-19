import streamlit as st
import requests

# 1. SAYFA YAPILANDIRMASI VE TEMA
st.set_page_config(page_title="Eğitim Bilimleri Makale Araması", page_icon="🎓", layout="wide")

# GAÜN Kurumsal Renkleri ve Stil Uygulaması
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #D32F2F;
        color: white;
    }
    .header-box {
        text-align: center; 
        padding: 30px; 
        background-color: #D32F2F; /* GAÜN Kırmızısı */
        border-radius: 10px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .footer-text {
        text-align: center;
        color: #333;
        font-weight: bold;
        margin-top: 10px;
    }
    </style>
    
    <div class="header-box">
        <h1 style='margin: 0; font-size: 40px;'>Eğitim Bilimleri Makale Araması</h1>
        <h2 style='margin: 10px 0 0 0; font-weight: normal;'>Prof. Dr. Bülent DÖŞ</h2>
        <p style='margin: 5px 0 0 0; font-size: 18px;'>Gaziantep University</p>
        <p style='margin: 5px 0 0 0; font-size: 16px; opacity: 0.9;'>✉️ bulentdos@yahoo.com</p>
    </div>
    """, unsafe_allow_html=True)

# 2. ARAMA PANELİ
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    q_in = st.text_input("Arama Terimi (Başlıkta Tam Eşleşme):", placeholder="Örn: teacher professional development")
with col2:
    min_c = st.number_input("Min. Atıf Sayısı:", value=0)
with col3:
    y_start = st.number_input("Yıl Filtresi:", value=2010)

st.markdown("---")

# 3. KESİN ARAMA MANTIĞI
if q_in:
    with st.spinner('Akademik veri tabanında kesin eşleşme aranıyor...'):
        # Çift tırnak ile tam kalıp araması yapıyoruz
        exact_query = f'"{q_in}"'
        url = f"https://api.openalex.org/works?filter=title.search:{exact_query},concepts.id:C17744445,type:article,publication_year:>{y_start}&sort=cited_by_count:desc&per-page=50"
        
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                res = r.json().get('results', [])
                
                # Sadece Sosyal Bilimler ve Eğitim odaklı tutmak için sağlık filtreleri
                ban = ['health', 'medical', 'clinical', 'nursing', 'patient', 'medicine', 'surgery', 'hospital', 'disease', 'physician', 'biomedical']
                
                final_results = []
                for w in res:
                    title = w.get('title', '')
                    s_info = (w.get('primary_location', {}).get('source', {}) or {})
                    s_name
