import streamlit as st
import pandas as pd
import os
from datetime import datetime
import time

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="IoT Çevre Analiz İstasyonu",
    page_icon="🌡️",
    layout="wide"
)

# --- VERİ YÜKLEME FONKSİYONU ---
def veriyi_getir():
    """
    Bugünün tarihli CSV dosyasını bulur ve yükler.
    """
    data_path = os.path.join("data", "raw")
    bugun = datetime.now().strftime('%Y%m%d')
    dosya_adi = f"sensor_log_{bugun}.csv"
    tam_yol = os.path.join(data_path, dosya_adi)

    if os.path.exists(tam_yol):
        try:
            df = pd.read_csv(tam_yol)
            # Zaman sütununu datetime formatına çevir
            df["Zaman"] = pd.to_datetime(df["Zaman"])
            return df
        except Exception as e:
            st.error(f"Veri okunurken hata oluştu: {e}")
            return None
    else:
        return None

# --- ARAYÜZ TASARIMI ---
st.title("🌱 IoT Tabanlı Çevre Analiz İstasyonu")
st.markdown("Raspberry Pi 5 & DHT11 Sensör Verileri")

# Veriyi Yükle
df = veriyi_getir()

if df is not None and not df.empty:
    # Son okunan değerleri al
    son_kayit = df.iloc[-1]
    
    # 1. BÖLÜM: METRİKLER (Kartlar)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="🌡️ Sıcaklık", value=f"{son_kayit['Sicaklik']} °C", delta=f"{df['Sicaklik'].diff().iloc[-1]:.1f} °C")
    
    with col2:
        st.metric(label="💧 Nem", value=f"% {son_kayit['Nem']}", delta=f"{df['Nem'].diff().iloc[-1]:.1f} %")
        
    with col3:
        st.metric(label="🕒 Son Güncelleme", value=son_kayit['Zaman'].strftime('%H:%M:%S'))

    st.divider()

    # 2. BÖLÜM: GRAFİKLER
    col_graph1, col_graph2 = st.columns(2)

    with col_graph1:
        st.subheader("Sıcaklık Değişimi (°C)")
        # Streamlit'in kendi line chart'ı çok hızlıdır
        st.line_chart(df, x="Zaman", y="Sicaklik", color="#FF4B4B")

    with col_graph2:
        st.subheader("Nem Değişimi (%)")
        st.line_chart(df, x="Zaman", y="Nem", color="#0068C9")

    # 3. BÖLÜM: VERİ TABLOSU (İsteğe bağlı açılır kapanır)
    with st.expander("📄 Ham Verileri Göster"):
        st.dataframe(df.sort_values(by="Zaman", ascending=False), use_container_width=True)

else:
    st.warning("⚠️ Bugün için henüz veri kaydı bulunamadı. 'main.py' çalışıyor mu?")
    st.info("Veri bekleniyor... Sayfayı yenileyebilirsiniz.")

# Otomatik Yenileme Butonu (Manuel)
if st.button('🔄 Verileri Şimdi Yenile'):
    st.rerun()