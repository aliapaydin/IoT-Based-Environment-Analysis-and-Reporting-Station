# 🌡️ IoT Tabanlı Ortam Analiz ve Raporlama İstasyonu

> **Raspberry Pi 5** üzerinde çalışan, 7/24 ortam sıcaklığı ve nem değerlerini kaydeden, analiz eden ve görselleştiren otomatik IoT istasyonu.

## 📋 Proje Özeti
Bu proje, **DHT11/DHT22** sensörleri kullanılarak ortam verilerinin toplanmasını, bu verilerin `.csv` formatında saklanmasını ve `Matplotlib/Seaborn` kütüphaneleri ile görselleştirilmesini sağlar. Sistem, **Systemd Servisi** olarak arka planda (headless) çalışacak şekilde tasarlanmıştır ve Raspberry Pi yeniden başlatılsa bile otomatik olarak devreye girer.

---

## 🛠️ Kullanılan Donanım ve Teknolojiler

### Donanım
* **Raspberry Pi 5 (8GB)**
* **DHT11 / DHT22** Sıcaklık ve Nem Sensörü
* Jumper Kablolar (Dişi-Erkek / Erkek-Erkek)

### Yazılım & Kütüphaneler
* **Dil:** Python 3.11+
* **Veri İşleme:** Pandas
* **Görselleştirme:** Matplotlib, Seaborn
* **Sensör Yönetimi:** Adafruit CircuitPython DHT, Adafruit Blinka
* **GPIO Yönetimi:** RPi.GPIO ve **rpi-lgpio** (Pi 5 özel çip desteği için)
* **Servis Yönetimi:** Systemd (Linux)

---

## 📂 Proje Yapısı
/IoT-Based-Environment-Analysis-and-Reporting-Station/ │ ├── data/ # Sensör verilerinin ve grafiklerin kaydedildiği klasör │ ├── sensor_verileri.csv │ └── sicaklik_nem_grafigi.png │ ├── src/ # Kaynak kodlar │ ├── sensor_gercek.py # Sensörden veri okuma modülü │ └── gorsellestirme.py # Grafik çizim modülü │ ├── venv/ # Python Sanal Ortamı (Virtual Environment) ├── main.py # Ana çalıştırma dosyası (Döngü burada) └── README.md # Proje dokümantasyonu
---

## 🚀 Kurulum Adımları (Baştan Sona)

Bu proje geliştirilirken karşılaşılan bağımlılık sorunlarını aşmak için aşağıdaki sıralama izlenmelidir.

### 1. Sistem Paketlerinin Yüklenmesi
Raspberry Pi 5 ve Python kütüphaneleri (özellikle Matplotlib ve GPIO) için gerekli sistem paketleri:

```bash
sudo apt update
sudo apt install python3-venv libopenjp2-7 libtiff6 libopenblas-dev liblgpio-dev -y
2. Sanal Ortamın (Venv) Kurulması
Sistem Python'unu kirletmemek için proje dizininde izole bir ortam oluşturulur:

Bash

cd ~/IoT-Based-Environment-Analysis-and-Reporting-Station
python3 -m venv venv
source venv/bin/activate
3. Python Kütüphanelerinin Yüklenmesi
Pi 5 mimarisi için rpi-lgpio ve görselleştirme araçları yüklenir:

Bash

pip install pandas matplotlib seaborn adafruit-circuitpython-dht adafruit-blinka rpi-lgpio --prefer-binary
⚙️ Systemd Servisi (Otomatik Başlatma)
Sistemin 7/24 arka planda çalışması için /etc/systemd/system/iot-station.service dosyası yapılandırılmıştır.

Servis Dosyası İçeriği:

Ini, TOML

[Unit]
Description=IoT Ortam Analiz Istasyonu
After=network.target

[Service]
# Python çıktılarını anlık görmek için -u parametresi kullanıldı
ExecStart=/home/aliapaydin/IoT-Based-Environment-Analysis-and-Reporting-Station/venv/bin/python -u /home/aliapaydin/IoT-Based-Environment-Analysis-and-Reporting-Station/main.py
WorkingDirectory=/home/aliapaydin/IoT-Based-Environment-Analysis-and-Reporting-Station
StandardOutput=inherit
StandardError=inherit
Restart=always
User=aliapaydin

[Install]
WantedBy=multi-user.target
Servis Komutları:

Başlatma: sudo systemctl start iot-station.service

Durdurma: sudo systemctl stop iot-station.service

Log İzleme: journalctl -u iot-station.service -f
🐛 Karşılaşılan Zorluklar ve Çözümler (Troubleshooting)
Bu projenin geliştirilmesi sırasında Raspberry Pi 5 mimarisi ve Linux servis yapısından kaynaklı kritik hatalar çözülmüştür:

1. Raspberry Pi 5 GPIO Hatası (ModuleNotFoundError: lgpio)
Sorun: Pi 5, eski RPi.GPIO kütüphanesini doğrudan desteklemeyen yeni bir çip yapısına (RP1) sahiptir.

Çözüm: liblgpio-dev sistem paketi kuruldu ve Python tarafında pip install rpi-lgpio kullanılarak uyumluluk sağlandı.

2. Servis Yol Hatası (203/EXEC)
Sorun: Systemd, Python komutunu bulamadı.

Çözüm: Servis dosyasında python yerine, sanal ortamın tam yolu (/home/.../venv/bin/python) belirtildi.

3. Matplotlib Bağımlılıkları (ImportError: libopenjp2.so.7)
Sorun: Grafik kütüphanesi, Linux tarafında eksik olan C kütüphaneleri yüzünden çalışmadı.

Çözüm: apt install libopenjp2-7 vb. komutlarla eksik sistem kütüphaneleri yüklendi.

4. EOFError (Input Hatası)
Sorun: Kod servise dönüştürüldüğünde, arka planda klavye girişi (input()) beklediği için çöktü.

Çözüm: main.py içerisindeki menü yapısı kaldırıldı, yerine sonsuz döngüde çalışan otomatik mod kodlandı.

5. Logların Görünmemesi (Buffering)
Sorun: Python çıktıları (print) journalctl loglarına geç düşüyordu.

Çözüm: Servis komutuna -u (unbuffered) parametresi eklendi.

📊 Örnek Çıktı (Loglar)
Sistem çalıştığında terminal logları şu şekildedir:

Plaintext

IoT İstasyonu Servis Modunda Başlatıldı
Otomatik Döngü: Kayıt + Analiz
========================================
[Mon Jan 19 00:01:10 2026] İşlem başlıyor...
>> Sensör verisi okunuyor ve kaydediliyor...
💾 KAYDEDİLDİ: 2026-01-19 00:02:10 | 25.6°C | %47
>> Grafikler çiziliyor...
>> İşlem başarılı. Bir sonraki döngü bekleniyor...
👨‍💻 Geliştirici
Ali Apaydın Tarih: 19 Ocak 2026
