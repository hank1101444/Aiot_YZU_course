import RPi.GPIO as GPIO
import time



flag = 0

def ButtonPressed(btn):
    global flag
    flag = (flag + 1) % 3
    print("Button pressed @",time.ctime())

GPIO.setmode(GPIO.BOARD)
BTN_PIN = 11
LED_PINS = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PINS, GPIO.OUT)
GPIO.setup(BTN_PIN,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(BTN_PIN,GPIO.FALLING,ButtonPressed,200)

try:
    while True:
        if flag == 0:
            GPIO.output(LED_PINS, GPIO.HIGH)
            time.sleep(0.5)
            print("0.5 speed")
            GPIO.output(LED_PINS, GPIO.LOW)
            time.sleep(0.5)
            print("0.5 speed")
        elif flag == 1:
            GPIO.output(LED_PINS, GPIO.HIGH)
            time.sleep(1)
            print("1 speed")

            GPIO.output(LED_PINS, GPIO.LOW)
            time.sleep(1)
            print("1 speed")
        else:
            GPIO.output(LED_PINS, GPIO.HIGH)
            time.sleep(2)
            print("2 speed")
            GPIO.output(LED_PINS, GPIO.LOW)
            time.sleep(2)
            print("2 speed")
except KeyboardInterrupt:
    print("Exception: Key")

finally:
    GPIO.cleanup()

