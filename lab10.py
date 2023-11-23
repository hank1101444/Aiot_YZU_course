import speech_recognition as sr
from gtts import gTTS
import os
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
LED_PINS = 32
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PINS, GPIO.OUT)




#obtain audio from the microphone
r=sr.Recognizer()
while(1):
    with sr.Microphone() as source:
        print("Please wait. Calibrating microphone...")
        #listen for 1 seconds and create the ambient noise energy level
        r.adjust_for_ambient_noise(source, duration=1)
        print("Say something!")
        audio=r.listen(source)
        # recognize speech using Google Speech Recognition
        res = r.recognize_google(audio, language='zh-TW')
        print(res)
        if("開燈") in res:    
            tts = gTTS(text='開燈', lang='zh-TW')
            tts.save('on.mp3')
            os.system('omxplayer -o local -p on.mp3 > /dev/null 2>&1')
            GPIO.output(LED_PINS, GPIO.HIGH)
            time.sleep(1)
            
        if("關燈") in res:
            tts = gTTS(text='關燈', lang='zh-TW')
            tts.save('off.mp3')
            os.system('omxplayer -o local -p off.mp3 > /dev/null 2>&1')
            GPIO.output(LED_PINS, GPIO.LOW)
            time.sleep(1)
        else :
            tts = gTTS(text=res, lang='zh-TW')
            tts.save('res.mp3')
            os.system('omxplayer -o local -p res.mp3 > /dev/null 2>&1')
            GPIO.output(LED_PINS, GPIO.LOW)
            time.sleep(1)


try:
    print("Google Speech Recognition thinks you said:")
    print(r.recognize_google(audio, language='zh-TW'))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("No response from Google Speech Recognition service: {0}".format(e))
finally:
    GPIO.cleanup()

