import streamlit as st
import requests

# Sayfa Ayarları
st.set_page_config(page_title="Prof. Dr. Bülent DÖŞ | Eğitim Bilimleri", page_icon="🎓", layout="wide")

# Başlık
st.markdown("""
    <div style='text-align: center; padding: 25px; background-color: #0E1117; border-radius: 15px; border: 1px solid #36393E;'>
        <h1 style='color: #FF4B4B; margin: 0;'>🎓 Eğitim Bilimleri Arama Motoru</h1>
        <p style='color: #808495;'>Prof. Dr. Bülent DÖŞ - Stabil Eğitim Literatürü Filtresi</p>
    </div>
    """, unsafe_allow_html=True)

# Panel
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    query = st.text_input("Makale Başlığında Ara:", placeholder="Örn: 'Curriculum' veya 'Teacher Training'")
with col2:
    min_cite = st.number_input("Min. Atıf:", min_value=0, value=0)
with col3:
    start_year = st.number_input("Başlangıç Yılı:", min_value=1950, value=2015)

st.markdown("---")

if query:
    with st.spinner('Makaleler taranıyor...'):
        # Sorguyu basit ve hızlı hale getirdik (Veritabanı hatasını önlemek için)
        url = f"https://api.openalex.org/works?filter=title.search:{query},concepts.id:C17744445,type:article&sort=cited_by_count:desc&per-page=100"
        
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                results = r.json().get('results', [])
                
                # SIKI EĞİTİM FİLTRESİ (Kod tarafında temizlik)
                # İçinde sağlık, tıp, diyet geçenleri ekrana hiç yansıtmıyoruz.
                final_list = []
                ban_keywords = ['diet', 'health', 'medical', 'weight', 'clinical', 'obesity', 'patient', 'surgery', 'nursing']
                
                for work in results:
                    source_name = (work.get('primary_location', {}).get('source', {}) or {}).get('display_name', '').lower()
                    title_lower = (work.get('title') or '').lower()
                    
                    # Eğer dergi adında veya başlıkta yasaklı kelime yoksa listeye al
                    if not any(bad in source_name for bad in ban_keywords) and not any(bad in title_lower for bad in ban_keywords):
                        final_list.append(work)
                
                # Sadece ilk 50'yi göster (temizlik sonrası)
                final_list = final_list[:50]

                if final_list:
                    st.success(f"Eğitim bilimleri odaklı {len(final_list)} nitelikli makale bulundu.")
                    for work in final_list:
                        t = work.get('title') or "Başlıksız"
                        y = work.get('publication_year') or "Bilinmiyor"
                        c = work.get('cited_by_count') or 0
                        d = work.get('doi') or "#"
                        sn = (work.get('primary_location', {}).get('source', {}) or {}).get('display_name', 'Eğitim Dergisi')

                        with st.container():
                            st.markdown(f"### 📄 {t}")
                            cl, cr = st.columns([4,
