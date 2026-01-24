from gpiozero import DigitalOutputDevice, DigitalInputDevice
from time import sleep

# Pin Tanımları (GPIO 17 ve 27)
PIN_OUT_NUM = 17
PIN_IN_NUM = 27

print(f"--- Pi 5 Pin Testi: GPIO {PIN_OUT_NUM} -> GPIO {PIN_IN_NUM} ---")

try:
    # Çıkış Pini (Sinyal gönderen)
    sender = DigitalOutputDevice(PIN_OUT_NUM)
    
    # Giriş Pini (Sinyal okuyan - Pull Down direnci ile)
    # pull_up=False demek, varsayılan olarak 0 okusun demektir.
    receiver = DigitalInputDevice(PIN_IN_NUM, pull_up=False)

    print("Test 1: Sinyal Gönderiliyor (HIGH)...")
    sender.on()
    sleep(0.5)
    
    if receiver.value == 1:
        print(f"✅ BAŞARILI: {PIN_OUT_NUM} pininden gönderilen sinyal {PIN_IN_NUM} pininden okundu.")
    else:
        print(f"❌ HATA: {PIN_OUT_NUM} pini aktif ama {PIN_IN_NUM} sinyali alamadı!")

    print("-" * 20)

    print("Test 2: Sinyal Kesiliyor (LOW)...")
    sender.off()
    sleep(0.5)
    
    if receiver.value == 0:
        print(f"✅ BAŞARILI: Sinyal kesildi ve {PIN_IN_NUM} pini 0 okudu.")
    else:
        print(f"❌ HATA: Sinyal kesildi ama {PIN_IN_NUM} hala 1 okuyor (Kısa devre olabilir)!")

    # Temizlik (gpiozero otomatik yapar ama biz yine de kapatalım)
    sender.close()
    receiver.close()

except Exception as e:
    print(f"Bir hata oluştu: {e}")