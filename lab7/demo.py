# Origin : http://blog.miguelgrinberg.com/post/video-streaming-with-flask

from flask import Flask, render_template, Response
from camera_pi import Camera
import cv2
import base64
import numpy as np
import RPi.GPIO as GPIO
import time


app = Flask(__name__)
angle = 0

def ButtonPressed(btn):
    global angle
    angle = (angle+45) % 360
    print("Button pressed @",time.ctime())
#button
GPIO.setmode(GPIO.BOARD)
BTN_PIN = 11
GPIO.setup(BTN_PIN,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(BTN_PIN,GPIO.FALLING,ButtonPressed,200)


@app.route('/')
def index():
    return render_template('stream.html')


def gen(camera):
    global angle
    while True:
        frame = camera.get_frame()  # get image
        rows, cols = frame.shape[:2]
        M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
        rotation = cv2.warpAffine(frame, M, (cols, rows))



        ret, jpeg = cv2.imencode('.jpg', rotation)
        jpeg= jpeg.tostring()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
