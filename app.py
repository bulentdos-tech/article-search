import streamlit as st
import requests
import pandas as pd
from io import BytesIO

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Eğitim Bilimleri Makale Araması", layout="wide")

# 2. KURUMSAL BAŞLIK
st.markdown("""
    <style>
    .scopus-badge {
        background-color: #007396; color: white; padding: 2px 8px; 
        border-radius: 4px; font-weight: bold; font-size: 12px; margin-left: 10px;
    }
    </style>
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
    q_in = st.text_input("Arama Terimi (Başlıkta Tam Eşleşme):", placeholder="Örn: digital literacy")
with c2:
    min_c = st.number_input("Min. Atıf:", value=0)
with c3:
    y_start = st.number_input("Yıl Filtresi:", value=2010)

st.markdown("---")

# 4. ARAMA VE FİLTRELEME
if q_in:
    with st.spinner('Veriler hazırlanıyor ve analiz ediliyor...'):
        target_url = f'https://api.openalex.org/works?filter=title.search:"{q_in}",concepts.id:C17744445,type:article,publication_year:>{y_start}&sort=cited_by_count:desc&per-page=50'
        try:
            r = requests.get(target_url, timeout=15)
            if r.status_code == 200:
                data = r.json().get('results', [])
                ban = ['health', 'medical', 'clinical', 'nursing', 'patient', 'medicine', 'surgery', 'hospital']
                
                export_data = [] # Excel için liste
                
                for w in data:
                    title = w.get('title', '')
                    src_obj = (w.get('primary_location', {}).get('source', {}) or {})
                    src_name = src_obj.get('display_name', '')
                    cite = w.get('cited_by_count', 0)
                    year = w.get('publication_year')
                    doi = w.get('doi', '')
                    
                    if q_in.lower() in title.lower() and not any(b in src_name.lower() for b in ban):
                        if cite >= min_c:
                            # Q ve Scopus Analizi
                            q_val = "Q1" if cite >= 50 else ("Q2" if cite >= 15 else "İndeksli")
                            is_scopus = "Evet" if src_obj.get('issn') else "Hayır"
                            
                            export_data.append({
                                "Makale Adı": title,
                                "Dergi": src_name,
                                "Yıl": year,
                                "Atıf Sayısı": cite,
                                "Kalite (Q)": q_val,
                                "Scopus": is_scopus,
                                "DOI Link": doi
                            })
                
                if export_data:
                    # Excel İndirme Butonu
                    df = pd.DataFrame(export_data)
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        df.to_excel(writer, index=False, sheet_name='Makale Listesi')
                    
                    st.download_button(
                        label="📥 Sonuçları Excel (XLSX) Olarak İndir",
                        data=output.getvalue(),
                        file_name=f"{q_in.replace(' ','_')}_makaleler.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    
                    st.success(f"{len(export_data)} prestijli makale bulundu.")
                    for item in export_data:
                        with st.container():
                            q_color = "#D32F2F" if item["Kalite (Q)"] == "Q1" else "#2E7D32"
                            sc_badge = "<span class='scopus-badge'>🔹 SCOPUS</span>" if item["Scopus"] == "Evet" else ""
                            st.markdown(f"### 📄 {item['Makale Adı']}")
                            st.markdown(f"🏢 **Dergi:** {item['Dergi']} | 📅 **Yıl:** {item['Yıl']} | <span style='color:{q_color}; font-weight:bold;'>[{item['Kalite (Q)']}]</span> {sc_badge}", unsafe_allow_html=True)
                            ca, cb = st.columns([4, 1])
                            with ca:
                                if item["DOI Link"]: st.write(f"🔗 [Makaleye Git]({item['DOI Link']})")
                            with cb:
                                st.metric("Atıf", item["Atıf Sayısı"])
                            st.markdown("---")
                else:
                    st.warning("Sonuç bulunamadı.")
            else:
                st.error("Veri tabanı hatası.")
        except Exception as e:
            st.error(f"Bağlantı hatası: {e}")
else:
    st.info("Lütfen bir terim girerek aramayı başlatın.")

st.markdown("<p style='text-align: center; color: gray;'>© 2025 | Gaziantep Üniversitesi</p>", unsafe_allow_html=True)
