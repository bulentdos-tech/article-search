import streamlit as st
import requests

st.set_page_config(page_title="Prof. Dr. Bülent DÖŞ | Akademik Arama", page_icon="🔎", layout="wide")

st.markdown("""
    <div style='text-align: center; padding: 20px; background-color: #0E1117; border-radius: 15px; border: 1px solid #36393E;'>
        <h1 style='color: #FF4B4B; margin: 0;'>🔍 Akademik Literatür Arama Motoru</h1>
        <p style='color: #808495;'>Prof. Dr. Bülent DÖŞ - Global ve Yerel Akademik Arama</p>
    </div>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    query = st.text_input("Arama Terimi (Türkçe veya İngilizce):", placeholder="Örn: 'Uzaktan Eğitim' veya 'Distance Learning'")

with col2:
    # Türkçe makalelerin atıf sayıları genelde daha düşüktür, o yüzden varsayılanı 0 yapalım
    min_cite = st.number_input("Min. Atıf Sayısı:", min_value=0, value=0)

with col3:
    start_year = st.number_input("Başlangıç Yılı:", min_value=1950, max_value=2025, value=2010)

st.markdown("---")

if query:
    with st.spinner('Arama yapılıyor...'):
        # 'title.search' yerine daha geniş olan 'search' parametresine döndük
        # Böylece Türkçe anahtar kelimeler özetlerde geçiyorsa da bulur.
        url = f"https://api.openalex.org/works?search={query}&filter=cited_by_count:>{min_cite},publication_year:>{start_year}&sort=cited_by_count:desc&per-page=20"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                results = response.json().get('results', [])
                
                if results:
                    st.success(f"'{query}' ile ilgili {len(results)} sonuç listelendi.")
                    for work in results:
                        title = work.get('title')
                        source = work.get('primary_location', {}).get('source', {}).get('display_name', 'Bilimsel Kaynak')
                        
                        # Dil Bilgisi
                        lang = work.get('language', 'Belirtilmemiş')
                        
                        with st.container():
                            st.markdown(f"### 📄 {title}")
                            c1, c2 = st.columns([4, 1])
                            with c1:
                                st.write(f"🏢 **Kaynak:** :blue[{source}]")
                                st.write(f"📅 **Yıl:** {work.get('publication_year')} | 🌍 **Dil:** {lang.upper()}")
                                if work.get('doi'):
                                    st.write(f"🔗 [Makaleye Git]({work.get('doi')})")
                            with c2:
                                st.metric("Atıf", work.get('cited_by_count'))
                            st.markdown("---")
                else:
                    st.warning("⚠️ Sonuç bulunamadı. Akademik veri tabanları çoğunlukla İngilizce indeksleme yapar. Lütfen terimin İngilizcesini de deneyin (Örn: 'Uzaktan Eğitim' yerine 'Distance Learning').")
            else:
                st.error("Ver
