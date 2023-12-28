import os
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import tensorflow as tf
import argparse
import sys
import pwm_motor as motor
import time
import ultrasound
import RPi.GPIO as GPIO
import object_detection_camera 
# Import utilites
sys.path.append('..')
from utils import label_map_util
from utils import visualization_utils as vis_util

detector = object_detection_camera.ObjectDetector(camera_type='usb')  # 可以改为 'picamera'
try:
    detector.detect_objects()
    sensor1 = ultrasound.UltrasonicSensor(31, 33)    #left trig echo
    sensor2 = ultrasound.UltrasonicSensor(22, 36)   #mid
    sensor3 = ultrasound.UltrasonicSensor(7, 15)   #right
    while True:
        left = sensor1.get_distance()
        print('left ok')
        right = sensor3.get_distance()
        print('right ok')
        mid = sensor2.get_distance()
        print('mid ok')
       
        print("{}{:.1f}{}".format("left 量測距離為: ", left, "公分"))
        print("{}{:.1f}{}".format("mid 量測距離為: ", mid, "公分"))
        print("{}{:.1f}{}".format("right 量測距離為: ", right, "公分\n\n"))
        motor.forward()
        if(mid < 15):
            motor.stop()
            time.sleep(0.5)
            if(left > right):
                motor.turnLeft(1)
            else:
                motor.turnRight(1)
            #print('stop!')
        if(left < 8):
            motor.modify_turnRight()
            #print('right')
        if(right < 8):
            motor.modify_turnLeft()
            #print('left')

finally:
    GPIO.cleanup()
    detector.cleanup() 
