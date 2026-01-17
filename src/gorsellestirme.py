import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# Veri klasörü
DATA_PATH = os.path.join("data", "raw")

def en_yeni_dosyayi_bul():
    """
    data/raw klasöründeki en son tarihli CSV dosyasını bulur.
    """
    dosyalar = glob.glob(os.path.join(DATA_PATH, "*.csv"))
    if not dosyalar:
        raise FileNotFoundError("Hiç veri dosyası (CSV) bulunamadı! Önce sensor_simulasyon.py çalıştırın.")
    
    # Dosyaları oluşturulma tarihine göre sırala ve en sonuncuyu al
    en_yeni_dosya = max(dosyalar, key=os.path.getctime)
    print(f"📂 Analiz edilen dosya: {en_yeni_dosya}")
    return en_yeni_dosya

def grafik_ciz():
    csv_dosyasi = en_yeni_dosyayi_bul()
    df = pd.read_csv(csv_dosyasi)

    # Zaman sütununu datetime formatına çevir (Grafikte düzgün görünsün)
    df["Zaman"] = pd.to_datetime(df["Zaman"])

    # Grafik Alanı Oluştur (2 satır, 1 sütun)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    # 1. Grafik: Sıcaklık
    ax1.plot(df["Zaman"], df["Sicaklik"], color="tab:red", marker="o", linestyle="-")
    ax1.set_title("Sıcaklık Değişimi (°C)")
    ax1.set_ylabel("Sıcaklık")
    ax1.grid(True, linestyle="--", alpha=0.6)

    # 2. Grafik: Nem
    ax2.plot(df["Zaman"], df["Nem"], color="tab:blue", marker="s", linestyle="-")
    ax2.set_title("Nem Değişimi (%)")
    ax2.set_ylabel("Nem")
    ax2.set_xlabel("Zaman")
    ax2.grid(True, linestyle="--", alpha=0.6)

    # Tarih formatını güzelleştir
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Grafiği göster
    print("📊 Grafik oluşturuluyor...")
    plt.show()

if __name__ == "__main__":
    grafik_ciz()