import streamlit as st
import requests

# Sayfa Yapılandırması
st.set_page_config(page_title="Prof. Dr. Bülent DÖŞ | Akademik Arama", page_icon="🔎", layout="wide")

# Başlık Paneli
st.markdown("""
    <div style='text-align: center; padding: 20px; background-color: #0E1117; border-radius: 15px; border: 1px solid #36393E;'>
        <h1 style='color: #FF4B4B; margin: 0;'>🔍 Akademik Literatür Arama Motoru</h1>
        <p style='color: #FAFAFA; font-size: 18px; opacity: 0.8;'>Küresel Veri Tabanlarında 50+ Nitelikli Sonuç</p>
        <p style='color: #808495;'>Geliştiren: <b>Prof. Dr. Bülent DÖŞ</b></p>
    </div>
    """, unsafe_allow_html=True)

# Arama Paneli
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    query = st.text_input("Arama Terimi (İngilizce önerilir):", placeholder="Örn: 'Distance Learning' veya 'Educational Technology'")

with col2:
    min_cite = st.number_input("Min. Atıf Sayısı:", min_value=0, value=5)

with col3:
    start_year = st.number_input("Başlangıç Yılı:", min_value=1950, max_value=2025, value=2015)

st.markdown("---")

if query:
    with st.spinner(f"'{query}' konusuyla ilgili en iyi 50 makale süzülüyor..."):
        # per-page parametresini 50 yaptık
        url = f"https://api.openalex.org/works?search={query}&filter=cited_by_count:>{min_cite},publication_year:>{start_year}&sort=cited_by_count:desc&per-page=50"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                if results:
                    st.success(f"Kriterlerinize uygun en popüler {len(results)} makale başarıyla listelendi.")
                    for work in results:
                        # Güvenli veri çekme
                        title = work.get('title') or "Başlıksız Makale"
                        year = work.get('publication_year') or "Bilinmiyor"
                        cites = work.get('cited_by_count') or 0
                        doi = work.get('doi') or "#"
                        
                        source_name = "Bilinmeyen Kaynak"
                        primary
