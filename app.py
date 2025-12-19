import streamlit as st
import requests

st.set_page_config(page_title="Prof. Dr. Bülent DÖŞ | Akademik Arama", page_icon="🔎", layout="wide")

st.markdown("""
    <div style='text-align: center; padding: 20px; background-color: #0E1117; border-radius: 15px; border: 2px solid #36393E;'>
        <h1 style='color: #FF4B4B; margin: 0;'>🔍 Akademik Literatür Arama Motoru</h1>
        <p style='color: #808495;'>Prof. Dr. Bülent DÖŞ - Eğitim Bilimleri Odaklı Arama</p>
    </div>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    query = st.text_input("Makale Konusu (İngilizce):", placeholder="Örn: 'Online Learning' veya 'Flipped Classroom'")

with col2:
    min_cite = st.number_input("Min. Atıf Sayısı:", min_value=0, value=10)

with col3:
    start_year = st.number_input("Başlangıç Yılı:", min_value=2000, max_value=2025, value=2018)

st.markdown("---")

if query:
    with st.spinner('Nitelikli makaleler getiriliyor...'):
        # DEĞİŞİKLİK: 'search' yerine 'title.search' kullanarak sadece başlıkta aratıyoruz.
        # Ayrıca per-page=25 ekleyerek sonuç sayısını artırdık.
        url = f"https://api.openalex.org/works?filter=title.search:{query},cited_by_count:>{min_cite},publication_year:>{start_year},type:article&sort=cited_by_count:desc&per-page=25"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                if results:
                    st.success(f"Başlığında '{query}' geçen en popüler {len(results)} makale bulundu.")
                    for work in results:
                        title = work.get('title')
                        source = work.get('primary_location', {}).get('source', {}).get('display_name', 'Bilimsel Dergi')
                        
                        with st.container():
                            st.markdown(f"### 📄 {title}")
                            c1, c2 = st.columns([4, 1])
                            with c1:
                                st.write(f"🏢 **Dergi:** :blue[{source}]")
                                st.write(f"📅 **Yıl:** {work.get('publication_year')} | 👤 **Yazar:** {work.get('authorships', [{}])[0].get('author', {}).get('display_name', 'Belirtilmemiş')}")
                                if work.get('doi'):
                                    st.write(f"🔗 [Makaleye Git]({work.get('doi')})")
                            with c2:
                                st.metric("Atıf", work.get('cited_by_count'))
                            st.markdown("---")
                else:
                    st.warning("Sonuç bulunamadı. Lütfen kelimeleri veya filtreleri kontrol edin.")
            else:
                st.error("Bağlantı sorunu.")
        except:
            st.error("Bir hata oluştu.")
else:
    st.info("Lütfen bir konu yazın.")
