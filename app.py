import streamlit as st
import requests

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Eğitim Bilimleri Makale Araması", page_icon="🎓", layout="wide")

# GAÜN KURUMSAL TASARIM
st.markdown("""
    <style>
    .header-box {
        text-align: center; padding: 25px; 
        background-color: #D32F2F; border-radius: 10px;
        color: white; margin-bottom: 20px;
    }
    </style>
    <div class="header-box">
        <h1 style='margin: 0;'>Eğitim Bilimleri Makale Araması</h1>
        <h2 style='margin: 5px; font-weight: normal;'>Prof. Dr. Bülent DÖŞ</h2>
        <p style='margin: 0;'>Gaziantep University</p>
        <p style='margin: 0; opacity: 0.9;'>✉️ bulentdos@yahoo.com</p>
    </div>
    """, unsafe_allow_html=True)

# 2. PANEL
c1, c2, c3 = st.columns([3, 1, 1])
with c1:
    q_in = st.text_input("Arama Terimi (Başlıkta Tam Eşleşme):", placeholder="Örn: peer learning")
with c2:
    min_c = st.number_input("Min. Atıf:", value=0)
with c3:
    y_start = st.number_input("Yıl:", value=2010)

st.markdown("---")

# 3. ARAMA MANTIĞI
if q_in:
    with st.spinner('Aranıyor...'):
        # Tam eşleşme için çift tırnaklı sorgu
        u = f'https://api.openalex.org/works?filter=title.search:"{q_in}",concepts.id:C17744445,type:article,publication_year:>{y_start}&sort=cited_by_count:desc&per-page=50'
        try:
            r = requests.get(u, timeout=15)
            if r.status_code == 200:
                res = r.json().get('results', [])
                ban = ['health', 'medical', 'clinical', 'nursing', 'patient', 'medicine', 'surgery', 'hospital']
                
                found = []
                for w in res:
                    title = w.get('title', '')
                    src = (w.get('primary_location', {}).get('source', {}) or {}).get('display_name', '').lower()
                    cite = w.get('cited_by_count', 0)
                    
                    # Hem başlıkta tam geçecek hem de tıp dergisi olmayacak
                    if q_in.lower() in title.lower() and not any(b in src for b in ban):
                        if cite >= min_c:
                            found.append(w)

                if found:
                    st.success(f"'{q_in}' ifadesi geçen {len(found)} makale bulundu.")
                    for w in found:
                        with st.container():
                            st.markdown(f"### 📄 {w.get('title')}")
                            ca, cb = st.columns([4, 1])
                            with ca:
                                sn = (w.get('primary_location', {}).get('source', {}) or {}).get('display_name', 'Eğitim Dergisi')
                                st.write(f"🏢 **Dergi:** :red[{sn}] | 📅 **Yıl:** {w.get('publication_year')}")
                                if w.get('doi'):
                                    st.write(f"🔗 [Makaleye Git]({w.get('doi')})")
                            with cb:
                                st.metric("Atıf", cite)
                            st.markdown("---")
                else:
                    st.warning("Eğitim bilimleri kriterlerinde tam eşleşme bulunamadı.")
            else:
                st.error("Veri tabanı yoğun, lütfen tekrar deneyin.")
        except Exception as e:
            st.error("Bir bağlantı hatası oluştu.")
else:
    st.info("Lütfen arama yapmak için bir terim girin.")

st.markdown("<p style='text-align: center; color: gray;'>© 2024 |
