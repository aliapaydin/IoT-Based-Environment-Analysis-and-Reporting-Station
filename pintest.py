import RPi.GPIO as GPIO
import time

# Pin Numaraları (BCM Modu)
PIN_A = 17
PIN_B = 27

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

def test_pins():
    print(f"--- Pin Testi Başlıyor: GPIO {PIN_A} <--> GPIO {PIN_B} ---")
    
    # SENARYO 1: A Çıkış, B Giriş
    GPIO.setup(PIN_A, GPIO.OUT)
    GPIO.setup(PIN_B, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    # A'yı HIGH yap, B'yi oku
    GPIO.output(PIN_A, GPIO.HIGH)
    time.sleep(0.1)
    if GPIO.input(PIN_B) == 1:
        print(f"[BAŞARILI] {PIN_A} HIGH gönderdi -> {PIN_B} HIGH okudu.")
    else:
        print(f"[HATA] {PIN_A} HIGH gönderdi ama {PIN_B} okuyamadı!")

    # A'yı LOW yap, B'yi oku
    GPIO.output(PIN_A, GPIO.LOW)
    time.sleep(0.1)
    if GPIO.input(PIN_B) == 0:
        print(f"[BAŞARILI] {PIN_A} LOW gönderdi -> {PIN_B} LOW okudu.")
    else:
        print(f"[HATA] {PIN_A} LOW gönderdi ama {PIN_B} okuyamadı!")

    print("-" * 30)

    # SENARYO 2: B Çıkış, A Giriş (Rolleri Değiş)
    GPIO.setup(PIN_B, GPIO.OUT)
    GPIO.setup(PIN_A, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # B'yi HIGH yap, A'yı oku
    GPIO.output(PIN_B, GPIO.HIGH)
    time.sleep(0.1)
    if GPIO.input(PIN_A) == 1:
        print(f"[BAŞARILI] {PIN_B} HIGH gönderdi -> {PIN_A} HIGH okudu.")
    else:
        print(f"[HATA] {PIN_B} HIGH gönderdi ama {PIN_A} okuyamadı!")

    GPIO.cleanup()

if __name__ == "__main__":
    try:
        setup()
        test_pins()
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        GPIO.cleanup()