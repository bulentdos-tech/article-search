import streamlit as st
import requests

st.set_page_config(page_title="Prof. Dr. Bülent DÖŞ | Eğitim Bilimleri", page_icon="🎓", layout="wide")

st.markdown("""
    <div style='text-align: center; padding: 25px; background-color: #0E1117; border-radius: 15px; border: 1px solid #36393E;'>
        <h1 style='color: #FF4B4B; margin: 0;'>🎓 Eğitim Bilimleri Arama Motoru</h1>
        <p style='color: #808495;'>Prof. Dr. Bülent DÖŞ - Saf Eğitim Literatürü Filtresi</p>
    </div>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    query = st.text_input("Eğitim Bilimlerinde Başlık Ara:", placeholder="Örn: 'Curriculum development' veya 'Classroom management'")
with col2:
    min_cite = st.number_input("Min. Atıf:", min_value=0, value=0)
with col3:
    start_year = st.number_input("Başlangıç Yılı:", min_value=1950, value=2010)

st.markdown("---")

if query:
    with st.spinner('Filtreler uygulanıyor, sağlık ve mühendislik eleniyor...'):
        # GÜNCELLEME: 
        # 1. 'title.search' ile sadece başlığa odaklandık.
        # 2. '!concepts.id:C71924100' (Tıp) ve '!concepts.id:C192562144' (Psikiyatri) gibi alanları yasakladık (!)
        # 3. 'concepts.id:C17744445' (Eğitim) şartını koruduk.
        
        forbidden = "!concepts.id:C71924100,!concepts.id:C192562144,!concepts.id:C33923547,!concepts.id:C41008148" # Tıp, Psikiyatri, Mühendislik, Bilgisayar Bilimi yasakları
        url = f"https://api.openalex.org/works?filter=title.search:{query},concepts.id:C17744445,type:article,{forbidden}&sort=cited_by_count:desc&per-page=50"
        
        if start_year:
            url += f",publication_year:>{start_year}"
            
        try:
            r = requests.get(url)
            if r.status_code == 200:
                results = r.json().get('results', [])
                
                # İkinci bir emniyet kilidi: Dergi adında sağlık kelimeleri geçenleri SİL
                education_only = []
                ban_words = ['health', 'weight', 'medical', 'clinical', 'physician', 'diet', 'obesity', 'medicine', 'nursing', 'surgery', 'patient']
                
                for w in results:
                    source_name = (w.get('primary_location', {}).get('source', {}) or {}).get('display_name', '').lower()
                    if not any(word in source_name for word in ban_words):
                        education_only.append(w)
                
                if education_only:
                    st.success(f"Eğitim bilimleri alanında '{query}' başlığıyla {len(education_only)} sonuç bulundu.")
                    for work in education_only:
                        t = work.get('title') or "Başlıksız"
                        y = work.get('publication_year') or "Bilinmiyor"
                        c = work.get('cited_by_count') or 0
                        d = work.get('doi') or "#"
                        sn = (work.get('primary_location', {}).get('source', {}) or {}).get('display_name', 'Eğitim Dergisi')

                        with st.container():
                            st.markdown(f"### 📄 {t}")
                            cl, cr = st.columns([4, 1])
                            with cl:
                                st.write(f"🏢 **Dergi:** :blue[{sn}]")
                                st.write(f"📅 **Yıl:** {y}")
                                if d != "#":
                                    st.markdown(f"[🔗 Makaleyi Görüntüle]({d})")
                            with cr:
                                st.metric("Atıf", c)
                            st.markdown("---")
                else:
                    st.warning("Eğitim bilimleri kriterlerinde sonuç bulunamadı.")
            else:
                st.error("Veri tabanı hatası.")
        except Exception as e:
            st.error("Bir bağlantı sorunu oluştu.")
else:
    st.info("Eğitim bilimleri makaleleri için arama yapın.")
