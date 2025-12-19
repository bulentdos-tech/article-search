import streamlit as st
import requests
import pandas as pd

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Prof. Dr. Bülent DÖŞ | Akademik Arama", page_icon="🔎", layout="wide")

# Şık Bir Başlık Alanı
st.markdown("""
    <div style='text-align: center; padding: 30px; background-color: #0E1117; border-radius: 15px; border: 1px solid #36393E; margin-bottom: 25px;'>
        <h1 style='color: #FF4B4B; margin: 0;'>🔍 Akademik Literatür Arama Motoru</h1>
        <p style='color: #FAFAFA; font-size: 18px; opacity: 0.8;'>Nitelikli ve Atıf Odaklı Makale Sorgulama Sistemi</p>
        <p style='color: #808495;'>Geliştiren: <b>Prof. Dr. Bülent DÖŞ</b></p>
    </div>
    """, unsafe_allow_html=True)

# --- ARAMA PANELİ ---
col1, col2 = st.columns([3, 1])

with col1:
    query = st.text_input("Makale Konusu, Başlığı veya DOI Numarası:", placeholder="Örn: 'Artificial intelligence in education' veya 'Distance learning'")

with col2:
    min_cite = st.number_input("Min. Atıf Sayısı (Filtre):", min_value=0, value=10, step=5)

st.markdown("---")

# --- VERİ ÇEKME VE LİSTELEME ---
if query:
    with st.spinner('Küresel veri tabanları taranıyor, lütfen bekleyin...'):
        url = f"https://api.openalex.org/works?search={query}&filter=cited_by_count:>{min_cite}&sort=cited_by_count:desc"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                # Hata aldığınız 'get' kısmı burada kontrol altına alındı:
                results = data.get('results', []) if data else []
                
                if results:
                    st.success(f"Kriterlerinize uygun en prestijli {len(results)} çalışma bulundu.")
                    for work in results:
                        if not work: continue # Boş kayıtları atla
                        
                        title = work.get('title', 'Başlıksız Makale')
                        year = work.get('publication_year', 'Yıl Belirtilmemiş')
                        cites = work.get('cited_by_count', 0)
                        
                        # Dergi ismini güvenli çekme
                        primary_loc = work.get('primary_location') or {}
                        source = primary_loc.get('source') or {}
                        journal_name = source.get('display_name', 'Bilinmeyen Dergi')
                        
                        doi = work.get('doi')
                        
                        with st.container():
                            st.markdown(f"### 📄 {title}")
                            c_left, c_right = st.columns([4, 1])
                            with c_left:
                                st.write(f"🏢 **Dergi:** {journal_name}")
                                st.write(f"📅 **Yıl:** {year}")
                                if doi:
                                    st.markdown(f"[🔗 Makaleyi Görüntüle / PDF]({doi})")
                            with c_right:
                                st.metric("Atıf Sayısı", cites)
                            st.markdown("<hr style='border: 0.5px solid #36393E;'>", unsafe_allow_html=True)
                else:
                    st.warning("Bu kriterlere uygun sonuç bulunamadı.")
            else:
                st.error("Veri tabanı şu an yanıt vermiyor.")
        except Exception as e:
            st.error(f"Sistem Hatası: {e}")
else:
    st.info("Lütfen yukarıdaki kutuya aramak istediğiniz konuyu yazın.")

# --- BİLGİ NOTU ---
with st.expander("ℹ️ Bu Sistem Nasıl Çalışır?"):
    st.write("""
        Bu arama motoru, **OpenAlex** veri tabanını kullanarak dünya üzerindeki milyonlarca bilimsel makaleyi tarar. 
        Sıradan arama motorlarının aksine, sonuçları **atıf sayılarına göre** sıralayarak en nitelikli (genellikle Q1 ve Q2) çalışmaları en üstte gösterir.
    """)
