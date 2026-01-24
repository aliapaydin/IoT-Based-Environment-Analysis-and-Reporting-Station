import pandas as pd
import time
from datetime import datetime
import os
import board
import adafruit_dht

# --- AYARLAR ---
# Sensörü burada tanımlıyoruz AMA hata olursa aşağıda yöneteceğiz
sensor = None

def sensoru_baslat():
    """Sensör nesnesini güvenli şekilde başlatır"""
    global sensor
    try:
        if sensor is not None:
            sensor.exit() # Varsa eskisini kapat
        sensor = adafruit_dht.DHT11(board.D17)
    except Exception as e:
        print(f"Sensör başlatma hatası: {e}")

# İlk açılışta başlatmayı dene
sensoru_baslat()

DATA_PATH = os.path.join("data", "raw")
os.makedirs(DATA_PATH, exist_ok=True)

def veri_uret():
    global sensor
    try:
        # Sensör kopmuşsa tekrar başlatmayı dene
        if sensor is None:
            sensoru_baslat()
            time.sleep(2)

        sicaklik = sensor.temperature
        nem = sensor.humidity
        
        if sicaklik is not None and nem is not None:
            zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return {"Zaman": zaman, "Sicaklik": sicaklik, "Nem": nem}
        else:
            return None
            
    except RuntimeError:
        # Okuma hatası (Checksum vb.) normaldir
        return None
    except Exception as error:
        # Ciddi hata (Message queue hatası gibi) -> Sensörü sıfırla
        print(f"Kritik Sensör Hatası: {error}")
        sensor.exit()
        sensor = None # Sensörü boşa çıkar ki bir sonraki tur yeniden başlatsın
        return None

def tek_seferlik_kayit():
    bugun = datetime.now().strftime('%Y%m%d')
    dosya_adi = f"sensor_log_{bugun}.csv"
    tam_yol = os.path.join(DATA_PATH, dosya_adi)

    if not os.path.exists(tam_yol):
        df_baslangic = pd.DataFrame(columns=["Zaman", "Sicaklik", "Nem"])
        df_baslangic.to_csv(tam_yol, index=False)

    deneme_sayisi = 0
    # Deneme sayısını 5'e düşürelim ki sistem çok takılmasın
    while deneme_sayisi < 5: 
        veri = veri_uret()
        
        if veri is not None:
            print(f"💾 KAYDEDİLDİ: {veri['Zaman']} | {veri['Sicaklik']}°C | %{veri['Nem']}")
            df_yeni = pd.DataFrame([veri])
            df_yeni.to_csv(tam_yol, mode='a', header=False, index=False)
            return True
        
        else:
            print("⚠️ Sensör okunuyor... (Tekrar deneniyor)")
            time.sleep(2)
            deneme_sayisi += 1
            
    print("❌ Bu turda sensörden veri alınamadı.")
    return False