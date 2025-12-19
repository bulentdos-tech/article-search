import streamlit as st
import requests

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Prof. Dr. Bülent DÖŞ | Eğitim Bilimleri", page_icon="🎓", layout="wide")

# 2. ÜST BAŞLIK
st.markdown("""
    <div style='text-align: center; padding: 25px; background-color: #0E1117; border-radius: 15px; border: 1px solid #36393E;'>
        <h1 style='color: #FF4B4B; margin: 0;'>🎓 Eğitim Bilimleri Arama Motoru</h1>
        <p style='color: #FAFAFA; font-size: 18px; opacity: 0.8;'>Prof. Dr. Bülent DÖŞ - Akademik Literatür Tarama</p>
    </div>
    """, unsafe_allow_html=True)

# 3. KULLANICI GİRİŞ PANELİ
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    query = st.text_input("Makale Başlığında Ara:", placeholder="Örn: 'Curriculum development'")
with col2:
    min_cite = st.number_input("Min. Atıf:", min_value=0, value=0)
with col3:
    start_year = st.number_input("Başlangıç Yılı:", min_value=1950, value=2015)

st.markdown("---")

# 4. ARAMA VE AYIKLAMA SÜRECİ
if query:
    with st.spinner('Eğitim veri tabanları taranıyor...'):
        url = f"https://api.openalex.org/works?filter=title.search:{query},concepts.id:C17744445,type:article&sort=cited_by_count:desc&per-page=100"
        if start_year:
            url += f",publication_year:>{start_year}"
            
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                results = r.json().get('results', [])
                final_list = []
                
                # Sağlık ve tıp makalelerini ayıklayan kara liste
                ban_words = ['diet', 'health', 'medical', 'weight', 'clinical', 'obesity', 'patient', 'surgery', 'nursing', 'physician', 'hospital', 'disease']
                
                for work in results:
                    s_name = (work.get('primary_location', {}).get('source', {}) or {}).get('display_name', '').lower()
                    t_lower = (work.get('title') or '').lower()
                    cites = work.get('cited_by_count') or 0
                    
                    is_med = any(bad in s_name for bad in ban_words) or any(bad in t_lower for bad in ban_words)
                    
                    if not is_med and cites >= min_cite:
                        final_list.append(work)
                
                if final_list:
                    st.success(f"Eğitim bilimleri odaklı {len(final_list[:50])} çalışma bulundu.")
                    for work in final_list[:50]:
                        title_text = work.get('title', 'Başlıksız')
                        year_text = work.get('publication_year', 'Bilinmiyor')
                        cite_count = work.get('cited_by_count', 0)
                        doi_link = work.get('doi', '#')
                        
                        source_info = work.get('primary_location', {}) or {}
                        source_obj = source_info.get('source', {}) or {}
                        journal_name = source_obj.get('display_name', 'Eğitim
