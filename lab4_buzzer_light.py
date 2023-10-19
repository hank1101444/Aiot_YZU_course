#### echo.py
import time
import serial
import RPi.GPIO as GPIO
import time


LED_PIN = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN, GPIO.OUT)
pwm_led = GPIO.PWM(LED_PIN, 100)
current =0
pwm_led.start(current)


BUZZ_PIN = 16
pitches = [262, 294, 330, 349, 392, 440, 493, 523]
GPIO.setup(BUZZ_PIN, GPIO.OUT)

pwm_buzzer = GPIO.PWM(BUZZ_PIN, pitches[0])
pwm_buzzer.start(0)

def play(pitch, intv):
    pwm_buzzer.ChangeFrequency(pitch)
    time.sleep(intv)

    
ser = serial.Serial('/dev/ttyAMA1', baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS
                    )
try:
    # ser.write(b'Hello World\r\n')
    # ser.write(b'Serial Communication Using Raspberry Pi\r\n')
    while True:    
        data = ser.readline()
        data = data.decode("utf-8").strip()
        print(f"current: {data}")
        if data == "playc":
            pwm_buzzer.ChangeFrequency(pitches[0])
        elif data == "playd":
            pwm_buzzer.ChangeFrequency(pitches[1])
        elif data == "playe":
            pwm_buzzer.ChangeFrequency(pitches[2])
        elif data == "playf":
            pwm_buzzer.ChangeFrequency(pitches[3])
        elif data == "playg":
            pwm_buzzer.ChangeFrequency(pitches[4])
        elif data == "playa":
            pwm_buzzer.ChangeFrequency(pitches[5])
        elif data == "playb":
            pwm_buzzer.ChangeFrequency(pitches[6])
        elif data == "start":
            #print(1)
            pwm_buzzer.ChangeDutyCycle(50)
        elif data == 'stop':
            pwm_buzzer.ChangeDutyCycle(0)
        elif data == 'bri':
            current = current+50
            pwm_led.ChangeDutyCycle(current)
        elif data == 'dim':
            current = current-50
            pwm_led.ChangeDutyCycle(current)
        data = data.encode()
        ser.write(data)
        ser.flushInput()
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    ser.close()
pwm_led.stop()
pwm_buzzer.stop()
GPIO.cleanup()
