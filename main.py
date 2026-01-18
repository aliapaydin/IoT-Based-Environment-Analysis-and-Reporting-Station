import sys
import time
from src.sensor_gercek import kaydet
from src.gorsellestirme import grafik_ciz

def menu():
    print("\n" + "="*40)
    print("   IoT İSTASYONU YÖNETİM PANELİ")
    print("="*40)
    print("1. Yeni Veri Üret ve Kaydet")
    print("2. Mevcut Veriyi Analiz Et (Grafik)")
    print("3. Otomatik Mod (Üret + Analiz Et)")
    print("q. Çıkış")
    print("-" * 40)
    
    secim = input("Seçiminiz: ")
    return secim

def main():
    while True:
        secim = menu()
        
        if secim == '1':
            adet = int(input("Kaç adet veri üretilsin? (Örn: 20): "))
            kaydet(adet)
            print("\n✅ Veri üretimi tamamlandı.")
            
        elif secim == '2':
            try:
                grafik_ciz()
            except Exception as e:
                print(f"❌ Hata: {e}")
                
        elif secim == '3':
            print("\n🔄 Otomatik mod başlatılıyor...")
            kaydet(20) # 20 adet üretir
            time.sleep(1)
            grafik_ciz()
            
        elif secim.lower() == 'q':
            print("Çıkış yapılıyor... Görüşmek üzere! 👋")
            break
            
        else:
            print("❌ Geçersiz seçim, tekrar deneyin.")

if __name__ == "__main__":
    main()