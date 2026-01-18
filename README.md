cat << 'EOF' > /home/aliapaydin/IoT-Based-Environment-Analysis-and-Reporting-Station/README.md
# 🌡️ IoT Tabanlı Ortam Analiz ve Raporlama İstasyonu

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%205-C51A4A?style=for-the-badge&logo=raspberrypi&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active%20(Service)-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> **Raspberry Pi 5** mimarisi üzerinde çalışan; ortam verilerini toplayan, işleyen ve görselleştiren tam otomatik IoT sistemi.

---

## 📖 Proje Hakkında

Bu proje, bir ortamın sıcaklık ve nem değişimlerini **7/24 kesintisiz** takip etmek amacıyla geliştirilmiştir. Sistem, "Headless" (ekransız) modda çalışacak şekilde optimize edilmiş olup, topladığı verileri analiz ederek anlamlı grafiklere dönüştürür.

### 🌟 Temel Özellikler
* ✅ **Otomatik Veri Toplama:** Her 60 saniyede bir hassas ölçüm.
* ✅ **Kalıcı Depolama:** Verilerin `.csv` formatında tarih damgalı saklanması.
* ✅ **Görsel Analiz:** `Matplotlib` ve `Seaborn` ile otomatik grafik üretimi.
* ✅ **Servis Mimarisi:** `Systemd` ile arka planda, boot sırasında otomatik başlama.
* ✅ **Hata Toleransı:** Sensör okuma hatalarına karşı "Retry" mekanizması.

---

## 🏗️ Sistem Mimarisi

Verinin sensörden çıkıp rapora dönüşme süreci:

    A[DHT Sensör] -->|Veri Okuma| B(Raspberry Pi 5 / Python)
    B -->|İşleme & Kayıt| C{Veri Tabanı .csv}
    B -->|Görselleştirme| D[PNG Grafikler]
    B -->|Loglama| E[Systemd Journal]

🛠️ Donanım ve Yazılım Envanteri
Bileşen,Detaylar,Amaç
Ana Kart,Raspberry Pi 5 (8GB),İşlemci ve Yönetim Merkezi
Sensör,DHT11 / DHT22,Sıcaklık ve Nem Verisi
OS,Raspberry Pi OS (Bookworm),İşletim Sistemi
Dil,Python 3.11+,Ana Yazılım Dili
Kütüphane,rpi-lgpio,Pi 5 GPIO Kontrolü (Kritik)
Analiz,"Pandas, Matplotlib, Seaborn",Veri İşleme ve Grafik

📂 Proje Yapısı
/IoT-Based-Environment-Analysis-and-Reporting-Station/
├── 📂 data/                 # 💾 Tüm verilerin toplandığı yer
│   ├── sensor_verileri.csv  # Ham veri deposu
│   └── sicaklik_nem_grafigi.png # Güncel analiz grafiği
├── 📂 src/                  # 🧠 Modüler kaynak kodlar
│   ├── sensor_gercek.py     # Sensör sürücüsü
│   └── gorsellestirme.py    # Grafik motoru
├── 📂 venv/                 # 🐍 İzole Python ortamı
├── main.py                  # 🚀 Ana servis dosyası
└── README.md                # 📄 Dokümantasyon

🚀 Kurulum ve Yapılandırma
Bu proje, Raspberry Pi 5'in yeni RP1 çip mimarisine uygun olarak kurulmalıdır.

1. Sistem Gereksinimleri
Matplotlib ve GPIO için gerekli C kütüphaneleri:

sudo apt update
sudo apt install libopenjp2-7 libtiff6 libopenblas-dev liblgpio-dev -y

2. Sanal Ortam ve Kütüphaneler
python3 -m venv venv
source venv/bin/activate
# Pi 5 uyumlu GPIO ve Analiz araçları
pip install pandas matplotlib seaborn adafruit-circuitpython-dht adafruit-blinka rpi-lgpio --prefer-binary

3. Servis Kurulumu (Daemon)
Sistemi arka plana atmak için /etc/systemd/system/iot-station.service dosyası oluşturulur:

[Unit]
Description=IoT Ortam Analiz Istasyonu
After=network.target

[Service]
ExecStart=/home/aliapaydin/IoT-Based-Environment-Analysis-and-Reporting-Station/venv/bin/python -u /home/aliapaydin/IoT-Based-Environment-Analysis-and-Reporting-Station/main.py
WorkingDirectory=/home/aliapaydin/IoT-Based-Environment-Analysis-and-Reporting-Station
Restart=always
User=aliapaydin

[Install]
WantedBy=multi-user.target

💡 Karşılaşılan Sorunlar ve Çözümler (Troubleshooting)
Proje geliştirme sürecinde Raspberry Pi 5'e özgü yaşanan "Dependency Hell" (Bağımlılık Cehennemi) ve çözümleri:

Hata / Sorun,Sebep,Çözüm
ModuleNotFoundError: lgpio,Pi 5'in yeni GPIO yapısı eski kütüphaneleri desteklemiyor.,pip install rpi-lgpio ve apt install liblgpio-dev kullanıldı.
ImportError: libopenjp2...,"Matplotlib, Linux tabanlı C kütüphanelerini bulamadı.",Eksik paketler apt ile sisteme eklendi.
EOFError: reading a line,Servis modunda (Headless) input() komutu çalışmaz.,"Menü yapısı iptal edildi, tam otomatik döngüye geçildi."
Logların Geç Gelmesi,Python'un çıktı tamponlaması (buffering).,Servis komutuna -u (unbuffered) parametresi eklendi.

📊 Canlı Log Örneği
Sistem çalışırken journalctl üzerinden alınan anlık çıktı:

IoT İstasyonu Servis Modunda Başlatıldı
========================================
[Mon Jan 19 00:05:11 2026] İşlem başlıyor...
>> Sensör verisi okunuyor...
💾 KAYDEDİLDİ: 2026-01-19 00:05:11 | 25.5°C | %46
>> Grafikler güncellendi.
>> Beklemeye geçiliyor (60sn)...

Geliştirici: Ali Apaydın 2026 © IoT Environment Analysis Station Made with ❤️ & 🐍 on Raspberry Pi 5
