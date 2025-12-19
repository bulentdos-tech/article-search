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
    query = st.text_input("Arama Terimi (Türkçe veya İngilizce):", placeholder="Örn: 'Uzaktan Eğitim' veya 'Distance Learning'")

with col2:
    min_cite = st.number_input("Min. Atıf Sayısı:", min_value=0, value=0)

with col3:
    start_year = st.number_input("Başlangıç Yılı:", min_value=1950, max_value=2025, value=2010)

st.markdown("---")

# İşlem Bloğu
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
                        title = work.get('title', 'Başlıksız')
                        source_data = work.get('primary_location', {}).get('source', {})
                        source_name = source_data.get('display_name', 'Bilimsel Kaynak')
                        lang = work.get('language', 'Belirtilmemiş')
                        
                        with st.container():
                            st.markdown(f"### 📄 {title}")
                            c_left, c_right = st.columns([4, 1])
                            with c_left:
                                st.write(f"🏢 **Kaynak:** :blue[{source_name}]")
                                st.write(f"📅 **Yıl:** {work.get('publication_year')} | 🌍 **Dil:** {lang.upper()}")
                                if work.get('doi'):
                                    st.write(f"🔗 [Makaleyi Görüntüle]({work.get('doi')})")
                            with c_right:
                                st.metric("Atıf", work.get('cited_by_count'))
                            st.markdown("---")
                else:
                    st.warning("Sonuç bulunamadı. Lütfen İngilizce terimlerle aramayı deneyin.")
            else:
                st.error("Veri tabanı sunucusuna bağlanılamadı.")
        except Exception as e:
            st.error(f"Sistem Hatası: {e}")
else:
    st.info("Aramaya başlamak için yukarıdaki kutuya bir konu yazın.")

# Alt Bilgi
st.markdown("<div style='text-align: center; color: gray; font-size: 12px;'>Bu sistem OpenAlex API altyapısını kullanmaktadır.</div>", unsafe_allow_html=True)
