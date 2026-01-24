import time
from src.sensor_gercek import tek_seferlik_kayit

def main():
    print("========================================")
    print("📡 IoT Veri Toplayıcı Başlatıldı")
    print("💾 Veriler arka planda kaydediliyor...")
    print("📊 Grafikleri görmek için yeni terminalde Streamlit'i çalıştırın.")
    print("========================================")

    while True:
        try:
            # Sadece kayıt işlemini çağırıyoruz
            basarili = tek_seferlik_kayit()

            if basarili:
                print(f"[{time.strftime('%H:%M:%S')}] >> Veri eklendi. Uyku moduna geçiliyor...")
            else:
                print(f"[{time.strftime('%H:%M:%S')}] >> Veri alınamadı. Tekrar denenecek.")

        except KeyboardInterrupt:
            print("\n🛑 Program kullanıcı tarafından durduruldu.")
            break
        except Exception as e:
            print(f"⚠️ ANA DÖNGÜ HATASI: {e}")

        # 30 Saniye bekle (İsteğe göre 60 yapabilirsiniz)
        time.sleep(30)

if __name__ == "__main__":
    main()