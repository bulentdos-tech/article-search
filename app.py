import streamlit as st
import requests

# Sayfa Ayarları
st.set_page_config(page_title="Prof. Dr. Bülent DÖŞ | Akademik Arama", page_icon="🔎", layout="wide")

# Başlık
st.markdown("""
    <div style='text-align: center; padding: 20px; background-color: #0E1117; border-radius: 15px; border: 1px solid #36393E;'>
        <h1 style='color: #FF4B4B; margin: 0;'>🔍 Akademik Literatür Arama Motoru</h1>
        <p style='color: #808495;'>Prof. Dr. Bülent DÖŞ - Küresel Veri Tabanlarında 50+ Nitelikli Sonuç</p>
    </div>
    """, unsafe_allow_html=True)

# Panel
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    query = st.text_input("Arama Terimi:", placeholder="Örn: 'Distance Learning'")
with col2:
    min_cite = st.number_input("Min. Atıf:", min_value=0, value=5)
with col3:
    start_year = st.number_input("Başlangıç Yılı:", min_value=1950, value=2015)

st.markdown("---")

if query:
    with st.spinner('50 Nitelikli sonuç getiriliyor...'):
        url = f"https://api.openalex.org/works?search={query}&filter=cited_by_count:>{min_cite},publication_year:>{start_year}&sort=cited_by_count:desc&per-page=50"
        
        try:
            r = requests.get(url)
            if r.status_code == 200:
                results = r.json().get('results', [])
                if results:
                    st.success(f"En popüler {len(results)} makale bulundu.")
                    for work in results:
                        # Verileri çek ve eksikse 'Bilinmiyor' yaz
                        t = work.get('title') or "Başlıksız"
                        y = work.get('publication_year') or "Bilinmiyor"
                        c = work.get('cited_by_count') or 0
                        d = work.get('doi') or "#"
                        
                        # Kaynak kontrolü
                        source_name = "Bilinmeyen Kaynak"
                        loc = work.get('primary_location')
                        if loc and loc.get('source'):
                            source_name = loc.get('source').get('display_name') or "Bilinmeyen Dergi"

                        # Arayüz Kartı
                        with st.container():
                            st.markdown(f"### 📄 {t}")
                            cl, cr = st.columns([4, 1])
                            with cl:
                                st.write(f"🏢 **Dergi:** {source_name}")
                                st.write(f"📅 **Yıl:** {y}")
                                if d != "#":
                                    st.markdown(f"[🔗 Makaleyi Görüntüle]({d})")
                            with cr:
                                st.metric("Atıf", c)
                            st.markdown("---")
                else:
                    st.warning("Sonuç bulunamadı.")
            else:
                st.error("Veri tabanı hatası.")
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
else:
    st.info("Lütfen bir konu yazın.")
