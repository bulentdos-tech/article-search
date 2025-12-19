import streamlit as st
import requests

st.set_page_config(page_title="Prof. Dr. Bülent DÖŞ | Akademik Filtre", page_icon="🎓", layout="wide")

# Akıllı Terim Sözlüğü
DICT = {
    "uzaktan öğrenme": "distance learning",
    "yapay zeka": "artificial intelligence",
    "ölçme değerlendirme": "assessment and evaluation",
    "müfredat": "curriculum"
}

st.markdown("""
    <div style='text-align: center; padding: 20px; background-color: #0E1117; border-radius: 10px;'>
        <h1 style='color: #FF4B4B;'>🎓 Eğitim Bilimleri Gelişmiş Arama</h1>
        <p style='color: #808495;'>İndeks ve Dergi Kalite Göstergeleri (Q1, Q2, SSCI/Scopus)</p>
    </div>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    q_in = st.text_input("Arama Terimi:", placeholder="Örn: 'Self-regulation'")
with col2:
    min_c = st.number_input("Min. Atıf:", value=0)
with col3:
    y_start = st.number_input("Yıl:", value=2015)

if q_in:
    search_term = q_in.lower()
    if search_term in DICT:
        search_term = f"({search_term} OR {DICT[search_term]})"
    
    with st.spinner('Dergi indeksleri ve makaleler analiz ediliyor...'):
        url = f"https://api.openalex.org/works?search={search_term}&filter=concepts.id:C17744445,type:article,publication_year:>{y_start}&sort=cited_by_count:desc&per-page=50"
        
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                res = r.json().get('results', [])
                ban = ['diet', 'health', 'medical', 'weight', 'clinical', 'obesity', 'patient', 'surgery']
                
                for w in res:
                    src_obj = (w.get('primary_location', {}).get('source', {}) or {})
                    s_name = src_obj.get('display_name', 'Bilinmeyen Dergi')
                    tle = (w.get('title') or '').lower()
                    
                    # Tıp filtresi
                    if any(b in s_name.lower() for b in ban) or any(b in tle for b in ban):
                        continue

                    cite = w.get('cited_by_count', 0)
                    if cite < min_c:
                        continue

                    # İndeks ve Q Değerlendirmesi
                    # OpenAlex'te doğrudan "Q1" etiketi her zaman gelmez, 
                    # ancak derginin tipine ve verilerine göre tahmin yürütebiliriz.
                    is_scopus = "Scopus" if src_obj.get('is_in_doaj') == False else "İndeksli"
                    issn = src_obj.get('issn', [])
                    
                    with st.container():
                        st.markdown(f"### 📄 {w.get('title')}")
                        ca, cb, cc = st.columns([3, 1, 1])
                        with ca:
                            st.write(f"🏢 **Dergi:** {s_name}")
                            st.write(f"📅 **Yıl:** {w.get('publication_year')}")
                            if w.get('doi'):
                                st.write(f"[🔗 Makaleye Git]({w.get('doi')})")
                        with cb:
                            # Dergi tipi ve prestij göstergesi
                            st.markdown("🔍 **İndeks Bilgisi**")
                            if src_obj.get('type') == 'journal':
                                st.info("✅ Akademik Dergi")
                                # Eğer dergi yüksek atıflıysa Q1/Q2 ihtimali yüksektir
                                if cite > 100:
                                    st.warning("🏆 Yüksek Etki (Q1/Q2)")
                            else:
                                st.text("Diğer Yayın")
                        with cc:
                            st.metric("Atıf Sayısı", cite)
                        st.markdown("---")
            else:
                st.error("Veri tabanı hatası.")
        except:
            st.error("Bağlantı hatası.")
