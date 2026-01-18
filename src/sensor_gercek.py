import pandas as pd
import time
from datetime import datetime
import os
import random # Nem sensörümüz olmadığı için onu şimdilik simüle edeceğiz

# Verilerin kaydedileceği klasör
DATA_PATH = os.path.join("data", "raw")
os.makedirs(DATA_PATH, exist_ok=True)

def cpu_sicaklik_oku():
    """
    Raspberry Pi'nin işlemci sıcaklığını sistem dosyasından okur.
    """
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = f.read()
            # Değer 1000'e bölünmeli (Örn: 45000 -> 45.0 C)
            return float(temp) / 1000.0
    except:
        return 0.0

def veri_uret():
    """
    Gerçek CPU sıcaklığını ve simüle edilmiş nem verisini döndürür.
    """
    sicaklik = cpu_sicaklik_oku()
    
    # Şu an nem sensörümüz (DHT11) takılı olmadığı için 
    # Nemi rastgele üretiyoruz (Grafik boş kalmasın diye)
    nem = round(random.uniform(30.0, 50.0), 2)
    
    zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return {"Zaman": zaman, "Sicaklik": sicaklik, "Nem": nem}

def kaydet(kayit_sayisi=10):
    print(f"--- 🌡️ Gerçek CPU Sıcaklığı İzleniyor ({kayit_sayisi} Adet) ---")
    
    veriler = []
    
    for i in range(kayit_sayisi):
        veri = veri_uret()
        veriler.append(veri)
        print(f"[{i+1}/{kayit_sayisi}] 🕒 {veri['Zaman']} | 🔥 İşlemci: {veri['Sicaklik']}°C | 💧 Nem: %{veri['Nem']} (Simüle)")
        time.sleep(1) 
        
    df = pd.DataFrame(veriler)
    dosya_adi = f"sensor_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    tam_yol = os.path.join(DATA_PATH, dosya_adi)
    
    df.to_csv(tam_yol, index=False)
    print(f"\n✅ Veriler kaydedildi: {tam_yol}")

if __name__ == "__main__":
    kaydet(10)