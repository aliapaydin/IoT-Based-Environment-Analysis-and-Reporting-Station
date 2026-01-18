import time
# Önceki loglardan gördüğümüz importlar
from src.sensor_gercek import kaydet
from src.gorsellestirme import grafik_ciz

def main():
    print("========================================")
    print("IoT İstasyonu Servis Modunda Başlatıldı")
    print("Otomatik Döngü: Kayıt + Analiz")
    print("========================================")

    # Servisin sürekli çalışması için sonsuz döngü
    while True:
        try:
            print(f"\n[{time.ctime()}] İşlem başlıyor...")

            # 1. Adım: Sensörden veriyi oku ve kaydet
            print(">> Sensör verisi okunuyor ve kaydediliyor...")
            kaydet()

            # 2. Adım: Grafikleri oluştur/güncelle
            print(">> Grafikler çiziliyor...")
            grafik_ciz()

            print(">> İşlem başarılı. Bir sonraki döngü bekleniyor...")

        except Exception as e:
            # Hata olursa servis çökmesin, loga yazıp devam etsin
            print(f"HATA OLUŞTU: {e}")

        # 3. Adım: Bekleme Süresi (Saniye cinsinden)
        # Burayı isteğine göre değiştirebilirsin (Örn: 300 = 5 dakika)
        time.sleep(60)

if __name__ == "__main__":
    main()