import streamlit as st
import requests

st.set_page_config(page_title="Prof. Dr. Bülent DÖŞ | Kesin Arama", page_icon="🎓", layout="wide")

st.markdown("""
    <div style='text-align: center; padding: 20px; background-color: #0E1117; border-radius: 10px;'>
        <h1 style='color: #FF4B4B;'>🎓 Eğitim Bilimleri Kesin Arama</h1>
        <p style='color: #808495;'>Sadece Başlığında "Tam Olarak" Bu İfade Geçen Makaleler</p>
    </div>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    # Kullanıcıdan gelen terimi alıyoruz
    q_in = st.text_input("Arama Terimi (Başlıkta olduğu gibi yazın):", placeholder="Örn: peer learning")
with col2:
    min_c = st.number_input("Min. Atıf:", value=0)
with col3:
    y_start = st.number_input("Yıl:", value=2010)

if q_in:
    with st.spinner('Tam eşleşme aranıyor...'):
        # DEĞİŞİKLİK: Terimi çift tırnak içine alarak API'ye "bu kelime grubunu bozma" diyoruz.
        # title.search artık sadece başlıkta bu kalıbı arayacak.
        exact_query = f'"{q_in}"'
        url = f"https://api.openalex.org/works?filter=title.search:{exact_query},concepts.id:C17744445,type:article,publication_year:>{y_start}&sort=cited_by_count:desc&per-page=50"
        
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                res = r.json().get('results', [])
                
                # Sağlık ve alakasız dergi filtreleri
                ban = ['health', 'medical', 'clinical', 'nursing', 'patient', 'medicine', 'surgery', 'hospital', 'disease', 'physician']
                
                final_results = []
                for w in res:
                    title = w.get('title', '')
                    s_name = (w.get('primary_location', {}).get('source', {}) or {}).get('display_name', '').lower()
                    
                    # 1. Kontrol: Başlıkta tam kelime grubu geçiyor mu? (Büyük/Küçük harf duyarsız)
                    if q_in.lower() in title.lower():
                        # 2. Kontrol: Sağlık dergisi mi?
                        if not any(bad in s_name for bad in ban):
                            if w.get('cited_by_count', 0) >= min_c:
                                final_results.append(w)

                if final_results:
                    st.success(f"Başlığında tam olarak '{q_in}' geçen {len(final_results)} makale bulundu.")
                    for w in final_results:
                        with st.container():
                            st.markdown(f"### 📄 {w.get('title')}")
                            ca, cb = st.columns([4, 1])
                            with ca:
                                sn = (w.get('primary_location', {}).get('source', {}) or {}).get('display_name', 'Eğitim Dergisi')
                                st.write(f"🏢 **Dergi:** {sn} | 📅 **Yıl:** {w.get('publication_year')}")
                                if w.get('doi'):
                                    st.write(f"[🔗 Makaleye Git]({w.get('doi')})")
                            with cb:
                                st.metric("Atıf", w.get('cited_by_count', 0))
                            st.markdown("---")
                else:
                    st.warning(f"Başlığında tam olarak '{q_in}' ifadesi geçen eğitim makalesi bulunamadı.")
            else:
                st.error("Veri tabanı hatası.")
        except:
            st.error("Bağlantı hatası.")
else:
    st.info("Lütfen bir terim girin.")
