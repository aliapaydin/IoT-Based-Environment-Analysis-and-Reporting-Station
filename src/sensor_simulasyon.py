import pandas as pd
import numpy as np
import time
from datetime import datetime
import os

# Verilerin kaydedileceği klasörü belirle
DATA_PATH = os.path.join("data", "raw")
os.makedirs(DATA_PATH, exist_ok=True) # Klasör yoksa oluşturur

def veri_uret():
    """
    Sanki bir IoT cihazından geliyormuş gibi anlık
    Sıcaklık (20-30 C arası) ve Nem (%40-60 arası) verisi üretir.
    """
    sicaklik = np.round(np.random.uniform(20.0, 30.0), 2)
    nem = np.round(np.random.uniform(40.0, 60.0), 2)
    zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return {"Zaman": zaman, "Sicaklik": sicaklik, "Nem": nem}

def kaydet(kayit_sayisi=10):
    print(f"--- {kayit_sayisi} Adet Veri Simüle Ediliyor ---")
    
    veriler = []
    
    for i in range(kayit_sayisi):
        veri = veri_uret()
        veriler.append(veri)
        print(f"Okunan: {veri}")
        time.sleep(1) # 1 saniye bekle (Gerçekçi olması için)
        
    # Veriyi DataFrame'e çevirip CSV olarak kaydet
    df = pd.DataFrame(veriler)
    dosya_adi = f"sensor_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    tam_yol = os.path.join(DATA_PATH, dosya_adi)
    
    df.to_csv(tam_yol, index=False)
    print(f"\nVeriler başarıyla kaydedildi: {tam_yol}")

if __name__ == "__main__":
    kaydet(10) # 10 adet veri üretip kaydeder