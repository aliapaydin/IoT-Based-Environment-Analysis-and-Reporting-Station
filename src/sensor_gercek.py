import pandas as pd
import time
from datetime import datetime
import os
import board
import adafruit_dht

# Sensör Ayarları (GPIO 4 Pinine bağlı)
# DHT11 sensörünü tanımlıyoruz
sensor = adafruit_dht.DHT11(board.D4)

# Verilerin kaydedileceği klasör
DATA_PATH = os.path.join("data", "raw")
os.makedirs(DATA_PATH, exist_ok=True)

def veri_uret():
    """
    DHT11 sensöründen gerçek sıcaklık ve nem okur.
    Hata olursa tekrar dener.
    """
    try:
        # Sensörden okuma yap
        sicaklik = sensor.temperature
        nem = sensor.humidity
        
        # Bazen sensör None (boş) değer döndürebilir
        if sicaklik is not None and nem is not None:
            zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return {"Zaman": zaman, "Sicaklik": sicaklik, "Nem": nem}
        else:
            return None
            
    except RuntimeError as error:
        # DHT11 okuma hatası verirse (çok sık olur) devam et
        return None
    except Exception as error:
        sensor.exit()
        raise error

def kaydet():
    print(f"--- 🚀 IoT İstasyonu Başlatıldı (7/24 Kayıt Modu) ---")
    
    # Dosya adını başlatırken bir kere belirleyelim (Günlük dosya olsun)
    bugun = datetime.now().strftime('%Y%m%d')
    dosya_adi = f"sensor_log_{bugun}.csv"
    tam_yol = os.path.join(DATA_PATH, dosya_adi)
    
    # Eğer dosya yoksa başlıkları (header) ekleyerek oluştur
    if not os.path.exists(tam_yol):
        df_baslangic = pd.DataFrame(columns=["Zaman", "Sicaklik", "Nem"])
        df_baslangic.to_csv(tam_yol, index=False)

    while True: # Sonsuz döngü
        veri = veri_uret()
        
        if veri is not None:
            # Ekrana yaz (Loglarda görmek için)
            print(f"💾 KAYDEDİLDİ: {veri['Zaman']} | {veri['Sicaklik']}°C | %{veri['Nem']}")
            
            # Veriyi tek satırlık DataFrame yap
            df_yeni = pd.DataFrame([veri])
            
            # Mevcut CSV dosyasının altına ekle (append mode)
            df_yeni.to_csv(tam_yol, mode='a', header=False, index=False)
            
        else:
            print("⚠️ Sensör okuma hatası, tekrar deneniyor...")
        
        # 60 Saniye bekle (Dakikada 1 ölçüm idealdir, diski yormaz)
        time.sleep(60)

if __name__ == "__main__":
    # Parametre vermiyoruz, sonsuz çalışacak
    kaydet()