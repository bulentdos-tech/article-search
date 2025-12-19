import streamlit as st
import requests

st.set_page_config(page_title="Prof. Dr. Bülent DÖŞ", page_icon="🎓", layout="wide")

st.markdown("""
    <div style='text-align: center; padding: 20px; background-color: #0E1117; border-radius: 10px;'>
        <h1 style='color: #FF4B4B;'>🎓 Eğitim Bilimleri Arama Motoru</h1>
        <p style='color: #808495;'>Prof. Dr. Bülent DÖŞ - Akademik Yayın Tarama</p>
    </div>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    q = st.text_input("Makale Başlığında Ara:", placeholder="Örn: Curriculum development")
with col2:
    min_c = st.number_input("Min. Atıf:", value=0)
with col3:
    y_start = st.number_input("Yıl:", value=2015)

st.markdown("---")

if q:
    with st.spinner('Taranıyor...'):
        url = f"https://api.openalex.org/works?filter=title.search:{q},concepts.id:C17744445,type:article,publication_year:>{y_start}&sort=cited_by_count:desc&per-page=100"
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                res = r.json().get('results', [])
                final = []
                ban = ['diet', 'health', 'medical', 'weight', 'clinical', 'obesity', 'patient', 'surgery', 'nursing', 'physician', 'hospital', 'disease']
                
                for w in res:
                    src = (w.get('primary_location', {}).get('source', {}) or {}).get('display_name', 'Dergi').lower()
                    tle = (w.get('title') or '').lower()
                    cite = w.get('cited_by_count') or 0
                    if not any(b in src for b in ban) and not any(b in tle for b in ban):
                        if cite >= min_c:
                            final.append(w)
                
                if final:
                    st.success(f"{len(final[:50])} makale bulundu.")
                    for w in final[:50]:
                        with st.container():
                            st.subheader(f"📄 {w.get('title')}")
                            c_a, c_b = st.columns([4, 1])
                            with c_a:
                                s_name = (w.get('primary_location', {}).get('source', {}) or {}).get('display_name', 'Kaynak')
                                st.write(f"🏢 {s_name} | 📅 {w.get('publication_year')}")
                                if w.get('doi'):
                                    st.write(f"[🔗 Makaleye Git]({w.get('doi')})")
                            with c_b:
                                st.metric("Atıf", w.get('cited_by_count'))
                            st.markdown("---")
                else:
                    st.warning("Sonuç bulunamadı.")
        except:
            st.error("Bağlantı hatası.")
else:
    st.info("Arama terimi girin.")
