import streamlit as st
import requests

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Eğitim Bilimleri Makale Araması", layout="wide")

# 2. KURUMSAL BAŞLIK (GAÜN RENKLERİ)
st.markdown("""
    <div style='text-align: center; padding: 25px; background-color: #D32F2F; border-radius: 10px; color: white;'>
        <h1 style='margin: 0;'>Eğitim Bilimleri Makale Araması</h1>
        <h2 style='margin: 5px; font-weight: normal;'>Prof. Dr. Bülent DÖŞ</h2>
        <p style='margin: 0;'>Gaziantep University</p>
        <p style='margin: 0; opacity: 0.9;'>✉️ bulentdos@yahoo.com</p>
    </div>
    """, unsafe_allow_html=True)

# 3. ARAMA PANELİ
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([3, 1, 1])
with c1:
    q_in = st.text_input("Arama Terimi (Başlıkta Tam Eşleşme):", placeholder="Örn: peer learning")
with c2:
    min_c = st.number_input("Min. Atıf:", value=0)
with c3:
    y_start = st.number_input("Yıl Filtresi:", value=2010)

st.markdown("---")

# 4. ARAMA VE FİLTRELEME
if q_in:
    with st.spinner('Veri tabanı taranıyor...'):
        target_url = f'https://api.openalex.org/works?filter=title.search:"{q_in}",concepts.id:C17744445,type:article,publication_year:>{y_start}&sort=cited_by_count:desc&per-page=50'
        try:
            r = requests.get(target_url, timeout=15)
            if r.status_code == 200:
                data = r.json().get('results', [])
                ban = ['health', 'medical', 'clinical', 'nursing', 'patient', 'medicine', 'surgery', 'hospital']
                found_list = []
                
                for w in data:
                    title = w.get('title', '')
                    src = (w.get('primary_location', {}).get('source', {}) or {}).get('display_name', '').lower()
                    cite = w.get('cited_by_count', 0)
                    if q_in.lower() in title.lower() and not any(b in src for b in ban):
                        if cite >= min_c:
                            found_list.append(w)
                
                if found_list:
                    st.success(f"{len(found_list)} makale bulundu.")
                    for w in found_list:
                        with st.container():
                            st.markdown(f"### 📄 {w.get('title')}")
                            sn = (w.get('primary_location', {}).get('source', {}) or {}).get('display_name', 'Eğitim Dergisi')
                            st.write(f"🏢 **Dergi:** {sn} | 📅 **Yıl:** {w.get('publication_year')} | 📈 **Atıf:** {w.get('cited_by_count')}")
                            if w.get('doi'):
                                st.write(f"🔗 [Makaleyi Görüntüle]({w.get('doi')})")
                            st.markdown("---")
                else:
                    st.warning("Sonuç bulunamadı.")
            else:
                st.error("Veri tabanı hatası.")
        except:
            st.error("Bağlantı hatası oluştu.")
else:
    st.info("Lütfen bir terim girerek aramayı başlatın.")

st.markdown("<p style='text-align: center; color: gray;'>© 2025 | Gaziantep Üniversitesi</p>", unsafe_allow_html=True)
