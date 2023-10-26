'''
This Example sends harcoded data to Ubidots using the request HTTP
library.

Please install the library using pip install requests

Made by Jose García @https://github.com/jotathebest/
'''

import requests
import random
import time
import sys
import RPi.GPIO as GPIO
import time




'''
global variables
'''

ENDPOINT = "industrial.api.ubidots.com"
DEVICE_LABEL = "weather-station"
VARIABLE_LABEL = "led"
TOKEN = "BBUS-xaMbFA7UaNhKISOKedyJlfOGFvatJv" # replace with your TOKEN
DELAY = 1  # Delay in seconds


def post_var(payload, url=ENDPOINT, device=DEVICE_LABEL, token=TOKEN):
    try:
        url = "http://{}/api/v1.6/devices/{}".format(url, device)
        headers = {"X-Auth-Token": token, "Content-Type": "application/json"}

        attempts = 0
        status_code = 400

        while status_code >= 400 and attempts < 5:
            print("[INFO] Sending data, attempt number: {}".format(attempts))
            req = requests.post(url=url, headers=headers,
                                json=payload)
            status_code = req.status_code
            attempts += 1
            time.sleep(1)

        print("[INFO] Results:")
        print(req.text)
    except Exception as e:
        print("[ERROR] Error posting, details: {}".format(e))

flag = 0

def ButtonPressed(btn):
    global flag
    flag = (flag + 1) % 2
    print("Button pressed @",time.ctime())

GPIO.setmode(GPIO.BOARD)
BTN_PIN = 11
LED_PINS = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PINS, GPIO.OUT)
GPIO.setup(BTN_PIN,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(BTN_PIN,GPIO.FALLING,ButtonPressed,200)



def main():

    sensor_value = flag
    # Builds Payload and topíc
    payload = {VARIABLE_LABEL: sensor_value}
    print(f"led : {sensor_value}")
    # Sends data
    post_var(payload)


if __name__ == "__main__":
    if TOKEN == "...":
        print("Error: replace the TOKEN string with your API Credentials.")
        sys.exit()
    while True:
        main()
        time.sleep(DELAY)
    GPIO.cleanup()
