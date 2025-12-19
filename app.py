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
        # OpenAlex API - Atıf sayısına göre sıralı ve filtreli
        url = f"https://api.openalex.org/works?search={query}&filter=cited_by_count:>{min_cite}&sort=cited_by_count:desc"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                if results:
                    st.success(f"Kriterlerinize uygun en prestijli {len(results)} çalışma bulundu.")
                    
                    for work in results:
                        # Bilgileri ayıkla
                        title = work.get('title')
                        year = work.get('publication_year')
                        cites = work.get('cited_by_count')
                        source = work.get('primary_location', {}).get('source', {}).get('display_name', 'Bilinmeyen Dergi')
                        doi = work.get('doi')
                        
                        # Görsel Kart Tasarımı
                        with st.container():
                            st.markdown(f"### 📄 {title}")
                            c_left, c_right = st.columns([4, 1])
                            with c_left:
                                st.write(f"🏢 **Dergi:** {source}")
                                st.write(f"📅 **Yıl:** {year}")
                                if doi:
                                    st.markdown(f"[🔗 Makaleyi Görüntüle / PDF]({doi})")
                            with c_right:
                                st.metric("Atıf Sayısı", cites)
                            st.markdown("<hr style='border: 0.5px solid #36393E;'>", unsafe_allow_html=True)
                else:
                    st.warning("Bu atıf barajıyla eşleşen bir sonuç bulunamadı. Filtreyi düşürmeyi deneyebilirsiniz.")
            else:
                st.error("Veri tabanına şu an ulaşılamıyor. Lütfen az sonra tekrar deneyin.")
        except Exception as e:
            st.error(f"Hata: {e}")

# --- BİLGİ NOTU ---
with st.expander("ℹ️ Bu Sistem Nasıl Çalışır?"):
    st.write("""
        Bu arama motoru, **OpenAlex** veri tabanını kullanarak dünya üzerindeki milyonlarca bilimsel makaleyi tarar. 
        Sıradan arama motorlarının aksine, sonuçları **atıf sayılarına göre** sıralayarak en nitelikli (genellikle Q1 ve Q2) çalışmaları en üstte gösterir.
    """)
