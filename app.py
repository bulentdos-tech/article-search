import streamlit as st
import requests

# Sayfa Yapılandırması
st.set_page_config(page_title="Prof. Dr. Bülent DÖŞ | Akademik Arama", page_icon="🔎", layout="wide")

# Başlık Paneli
st.markdown("""
    <div style='text-align: center; padding: 20px; background-color: #0E1117; border-radius: 15px; border: 1px solid #36393E;'>
        <h1 style='color: #FF4B4B; margin: 0;'>🔍 Akademik Literatür Arama Motoru</h1>
        <p style='color: #808495;'>Prof. Dr. Bülent DÖŞ - Küresel Akademik Veri Tarama</p>
    </div>
    """, unsafe_allow_html=True)

# Arama Paneli
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    query = st.text_input("Arama Terimi (Türkçe veya İngilizce):", placeholder="Örn: 'Distance Learning'")

with col2:
    min_cite = st.number_input("Min. Atıf Sayısı:", min_value=0, value=0)

with col3:
    start_year = st.number_input("Başlangıç Yılı:", min_value=1950, max_value=2025, value=2010)

st.markdown("---")

if query:
    with st.spinner('Veri tabanları taranıyor...'):
        url = f"https://api.openalex.org/works?search={query}&filter=cited_by_count:>{min_cite},publication_year:>{start_year}&sort=cited_by_count:desc&per-page=20"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                if results:
                    st.success(f"'{query}' ile ilgili {len(results)} sonuç listelendi.")
                    for work in results:
                        # GÜVENLİ VERİ ÇEKME (NoneType hatasını bu bloklar engeller)
                        title = work.get('title') or "Başlıksız Makale"
                        year = work.get('publication_year') or "Bilinmiyor"
                        cites = work.get('cited_by_count') or 0
                        doi = work.get('doi') or "#"
                        
                        # Dergi ismini en derin katmana kadar kontrol ederek alıyoruz
                        source_name = "Bilinmeyen Kaynak"
                        primary_loc = work.get('primary_location')
                        if primary_loc:
                            source = primary_loc.get('source')
                            if source:
                                source_name = source.get('display_name') or "Bilinmeyen Dergi"
                        
                        lang = (work.get('language') or "Bilinmiyor").upper()
                        
                        with st.container():
                            st.markdown(f"### 📄 {title}")
                            c_left, c_right = st.columns([4, 1])
                            with c_left:
                                st.write(f"🏢 **Kaynak:** :blue[{source_name}]")
                                st.write(f"📅 **Yıl:** {year} | 🌍 **Dil:** {lang}")
                                if doi != "#":
                                    st.write(f"🔗 [Makaleyi Görüntüle]({doi})")
                            with c_right:
                                st.metric("Atıf", cites)
                            st.markdown("---")
                else:
                    st.warning("Sonuç bulunamadı.")
            else:
                st.error("Veri tabanı hatası.")
        except Exception as e:
            st.error(f"Sistem şu an meşgul, lütfen tekrar deneyin.")
else:
    st.info("Aramaya başlamak için yukarıdaki kutuya bir konu yazın.")
