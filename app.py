import streamlit as st
import requests

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Prof. Dr. Bülent DÖŞ | Eğitim Bilimleri", page_icon="🎓", layout="wide")

# 2. ÜST BAŞLIK ALANI
st.markdown("""
    <div style='text-align: center; padding: 25px; background-color: #0E1117; border-radius: 15px; border: 1px solid #36393E;'>
        <h1 style='color: #FF4B4B; margin: 0;'>🎓 Eğitim Bilimleri Arama Motoru</h1>
        <p style='color: #808495;'>Prof. Dr. Bülent DÖŞ - Akademik Literatür Tarama Sistemi</p>
    </div>
    """, unsafe_allow_html=True)

# 3. ARAMA PANELİ
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    query = st.text_input("Makale Başlığında Ara (İngilizce Terimler Daha İyi Sonuç Verir):", placeholder="Örn: 'Curriculum' veya 'Educational Leadership'")
with col2:
    min_cite = st.number_input("Min. Atıf:", min_value=0, value=0)
with col3:
    start_year = st.number_input("Başlangıç Yılı:", min_value=1950, value=2015)

st.markdown("---")

# 4. ARAMA VE FİLTRELEME MANTIĞI
if query:
    with st.spinner('Eğitim veri tabanları taranıyor...'):
        # API Sorgusu: Sadece Eğitim (C17744445) kavramını ve makaleleri (article) istiyoruz
        url = f"https://api.openalex.org/works?filter=title.search:{query},concepts.id:C17744445,type:article&sort=cited_by_count:desc&per-page=100"
        
        if start_year:
            url += f",publication_year:>{start_year}"
            
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                results = r.json().get('results', [])
                
                # EĞİTİM DIŞI ALANLARI AYIKLAMA (SAĞLIK, TIP, VB.)
                final_list = []
                ban_keywords = ['diet', 'health', 'medical', 'weight', 'clinical', 'obesity', 'patient', 'surgery', 'nursing', 'physician', 'hospital']
                
                for work in results:
                    source_name = (work.get('primary_location', {}).get('source', {}) or {}).get('display_name', '').lower()
                    title_lower = (work.get('title') or '').lower()
                    
                    # Filtreleme: Ne başlıkta ne dergi adında tıp terimi geçmemeli
                    if not any(bad in source_name for bad in ban_keywords) and not any(bad in title_lower for bad in ban_keywords):
