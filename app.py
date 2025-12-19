import streamlit as st
import requests

st.set_page_config(page_title="Prof. Dr. Bülent DÖŞ | Akademik Filtre", page_icon="🎓", layout="wide")

# Akıllı Terim Sözlüğü
DICT = {
    "uzaktan öğrenme": "distance learning",
    "yapay zeka": "artificial intelligence",
    "ölçme değerlendirme": "assessment and evaluation",
    "müfredat": "curriculum",
    "öğretmen eğitimi": "teacher education"
}

st.markdown("""
    <div style='text-align: center; padding: 20px; background-color: #0E1117; border-radius: 10px;'>
        <h1 style='color: #FF4B4B;'>🎓 Eğitim Bilimleri Gelişmiş Arama</h1>
        <p style='color: #808495;'>Dergi Kalite Göstergeleri: SSCI & Scopus Tahmini</p>
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
        # Sorguda kavramı eğitim (C17744445) olarak tutuyoruz
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

                    # İndeks Analizi
                    is_scopus = False
                    is_high_impact = False
                    
                    # Eğer derginin ISSN'si varsa ve OpenAlex'te indeks verisi doluysa
                    # Genellikle Scopus ve SSCI dergilerinin ISSN'si sistemde kayıtlıdır.
                    if src_obj.get('issn'):
                        is_scopus = True # ISSN varsa büyük ihtimalle Scopus/SSCI adayıdır
                    
                    # SJR (SCImago Journal Rank) verisi kalite için en iyi göstergedir
                    # Not: OpenAlex API'sinde bu bazen metadata içinde gelir.
                    
                    with st.container():
                        st.markdown(f"### 📄 {w.get('title')}")
                        ca, cb, cc = st.columns([3, 1, 1])
                        with ca:
                            st.write(f"🏢 **Dergi:** {s_name}")
                            st.write(f"📅 **Yıl:** {w.get('publication_year')}")
                            if w.get('doi'):
                                st.write(f"[🔗 Makaleye Git]({w.get('doi')})")
                        
                        with cb:
                            st.markdown("🔍 **İndeks Tahmini**")
                            if is_scopus:
                                st.success("🟢 Scopus / SSCI Adayı")
                                if cite > 50:
                                    st.warning("🏆 Q1/Q2 Potansiyeli")
                            else:
                                st.info("ℹ️ Diğer İndeks")
                        
                        with cc:
                            st.metric("Atıf", cite)
                        st.markdown("---")
                else:
                    if not res: st.warning("Sonuç bulunamadı.")
            else:
                st.error("Veri tabanı hatası.")
        except:
            st.error("Bağlantı hatası.")
