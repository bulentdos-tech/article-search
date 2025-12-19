import streamlit as st
import requests

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Prof. Dr. Bülent DÖŞ | Akademik Arama", page_icon="🔎", layout="wide")

st.markdown("""
    <div style='text-align: center; padding: 20px; background-color: #0E1117; border-radius: 15px; border: 1px solid #36393E;'>
        <h1 style='color: #FF4B4B; margin: 0;'>🔍 Akademik Literatür Arama Motoru</h1>
        <p style='color: #808495;'>Prof. Dr. Bülent DÖŞ</p>
    </div>
    """, unsafe_allow_html=True)

# --- ARAMA PANELİ ---
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    query = st.text_input("Makale Konusu (İngilizce önerilir):", placeholder="Örn: 'Distance Learning' veya 'Educational Technology'")

with col2:
    # Saçma sonuçları engellemek için min. atıf sayısını biraz yüksek tutalım (Örn: 20)
    min_cite = st.number_input("Min. Atıf Sayısı:", min_value=0, value=20)

with col3:
    # Çok eski makaleleri elemek için yıl filtresi
    start_year = st.number_input("Başlangıç Yılı:", min_value=1900, max_value=2025, value=2015)

st.markdown("---")

if query:
    with st.spinner('Nitelikli literatür süzülüyor...'):
        # URL'yi daha spesifik hale getirdik: Hem alakalılık hem atıf dengesi
        # Ayrıca dil ve döküman tipi filtresi eklenebilir
        url = f"https://api.openalex.org/works?search={query}&filter=cited_by_count:>{min_cite},publication_year:>{start_year}&sort=cited_by_count:desc"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                results = response.json().get('results', [])
                
                if results:
                    st.success(f"Kriterlere uygun en prestijli {len(results)} makale listelendi.")
                    for work in results:
                        # Başlıkta aranan kelime geçiyor mu kontrolü (Opsiyonel ama alakayı artırır)
                        title = work.get('title', 'Başlıksız')
                        
                        source = work.get('primary_location', {}).get('source', {})
                        journal_name = source.get('display_name', 'Bilimsel Dergi / Kaynak')
                        
                        with st.container():
                            st.markdown(f"### 📄 {title}")
                            c1, c2 = st.columns([4, 1])
                            with c1:
                                st.write(f"🏢 **Dergi:** :blue[{journal_name}]")
                                st.write(f"📅 **Yıl:** {work.get('publication_year')} | 👤 **Yazar:** {work.get('authorships', [{}])[0].get('author', {}).get('display_name', 'Belirtilmemiş')}")
                                if work.get('doi'):
                                    st.markdown(f"[🔗 Makaleye Git / Tam Metin]({work.get('doi')})")
                            with c2:
                                st.metric("Atıf", work.get('cited_by_count'))
                            st.markdown("---")
                else:
                    st.warning("Sonuç bulunamadı. Filtreleri (Yıl veya Atıf) düşürmeyi deneyin.")
            else:
                st.error("Bağlantı sorunu.")
        except:
            st.error("Bir hata oluştu.")
else:
    st.info("Lütfen bir konu yazın (Örn: 'Online education impact')")
