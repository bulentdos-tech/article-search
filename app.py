import streamlit as st
import requests

# Sayfa Ayarları
st.set_page_config(page_title="Prof. Dr. Bülent DÖŞ | Eğitim Bilimleri Portalı", page_icon="🎓", layout="wide")

# Başlık Paneli
st.markdown("""
    <div style='text-align: center; padding: 25px; background-color: #0E1117; border-radius: 15px; border: 1px solid #36393E;'>
        <h1 style='color: #FF4B4B; margin: 0;'>🎓 Eğitim Bilimleri Akademik Arama</h1>
        <p style='color: #808495;'>Prof. Dr. Bülent DÖŞ - Sosyal Bilimler ve Eğitim Odaklı Geniş Literatür</p>
    </div>
    """, unsafe_allow_html=True)

# Panel
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    query = st.text_input("Eğitim Alanında Ara (Örn: Sınıf Yönetimi, Ölçme Değerlendirme, AI):", placeholder="Örn: 'Curriculum development' veya 'Self-efficacy'")
with col2:
    min_cite = st.number_input("Min. Atıf:", min_value=0, value=0)
with col3:
    start_year = st.number_input("Başlangıç Yılı:", min_value=1950, value=2010)

st.markdown("---")

if query:
    with st.spinner(f"Eğitim bilimleri literatüründe '{query}' taranıyor..."):
        # GÜNCELLEME: Hem başlıkta hem de kavramda eğitim olan her şeyi getiriyoruz.
        # Healthcare, Engineering gibi alanları 'concepts' filtresiyle eledik.
        url = f"https://api.openalex.org/works?search={query}&filter=concepts.id:C17744445,type:article&sort=cited_by_count:desc&per-page=50"
        
        if start_year:
            url += f"&filter=publication_year:>{start_year}"
            
        try:
            r = requests.get(url)
            if r.status_code == 200:
                results = r.json().get('results', [])
                
                # Manuel temizlik: Tıp, biyoloji ve mühendislik terimlerini dergi adından süzüyoruz
                exclude_terms = ['health', 'medical', 'clinical', 'engineering', 'chemistry', 'physics', 'surgery']
                clean_results = [
                    w for w in results 
                    if not any(term in (w.get('primary_location', {}).get('source', {}) or {}).get('display_name', '').lower() for term in exclude_terms)
                ]
                
                if clean_results:
                    st.success(f"Eğitim bilimleri kapsamında en nitelikli {len(clean_results)} çalışma bulundu.")
                    for work in clean_results:
                        t = work.get('title') or "Başlıksız"
                        y = work.get('publication_year') or "Bilinmiyor"
                        c = work.get('cited_by_count') or 0
                        d = work.get('doi') or "#"
                        
                        source_name = (work.get('primary_location', {}).get('source', {}) or {}).get('display_name', 'Eğitim Kaynağı')

                        with st.container():
                            st.markdown(f"### 📄 {t}")
                            cl, cr = st.columns([4, 1])
                            with cl:
                                st.write(f"🏢 **Dergi:** :green[{source_name}]")
                                st.write(f"📅 **Yıl:** {y}")
                                if d != "#":
                                    st.markdown(f"[🔗 Makaleyi Görüntüle]({d})")
                            with cr:
                                st.metric("Atıf", c)
                            st.markdown("---")
                else:
                    st.warning("Bu konu eğitim bilimleri çerçevesinde bulunamadı.")
            else:
                st.error("Veri tabanı hatası.")
        except Exception as e:
            st.error(f"Bağlantı hatası: {e}")
else:
    st.info("Eğitim bilimleri araştırması yapmak için bir terim girin.")
