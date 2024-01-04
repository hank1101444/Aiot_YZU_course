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
import threading

# Import utilities
sys.path.append('../..')
sys.path.append('..')
from utils import label_map_util
from utils import visualization_utils as vis_util

# 定义一个标志来控制主程序
stop_program = False
left, right, mid = 9999, 9999, 9999
lock = threading.Lock()  # 新增一个锁
sensor1 = ultrasound.UltrasonicSensor(31, 33)  # 左超声波传感器 trig 和 echo 引脚
sensor2 = ultrasound.UltrasonicSensor(22, 36)  # 中间超声波传感器 trig 和 echo 引脚
sensor3 = ultrasound.UltrasonicSensor(7, 15)   # 右超声波传感器 trig 和 echo 引脚

def get_dis():
    global left, right, mid
    while not stop_program:
        with lock:
            left = sensor1.get_distance()        
            right = sensor3.get_distance()     
            mid = sensor2.get_distance()
        time.sleep(0.3)  # give time to modify the car pretend dead lock!

def run_program1():
    global stop_program
    try:
        while not stop_program:
            with lock:
                local_left, local_mid, local_right = left, mid, right

            print(f"左边测量距离为: {local_left:.1f}公分")
            print(f"中间测量距离为: {local_mid:.1f}公分")
            print(f"右边测量距离为: {local_right:.1f}公分\n\n")
            motor.forward(0.3)
            if local_mid < 15:
                motor.stop()
                time.sleep(0.5)
                print('fuck mid')
                # if local_left > local_right:
                #     motor.turnLeft(1)
                # else:
                #     motor.turnRight(1)
                # motor.stop()
            elif local_left < 10:
                print('fuck left\n')
                # motor.modify_turnRight()
                # motor.stop()
            elif local_right < 10:
                print('fuck right\n')
                # motor.modify_turnLeft()
                # motor.stop()
            time.sleep(0.1)  # 增加延时
    finally:
        print('fuck done')
        GPIO.cleanup()

def run_program2():
    try:
        cap = cv2.VideoCapture(0)   
        if not cap.isOpened():
            raise Exception("无法打开摄像头")

        while not stop_program:
            ret, frame = cap.read()
            if not ret:
                print("无法接收画面 (摄像头结束?). 退出...")
                break

            cv2.imshow('live', frame)

            if cv2.waitKey(1) == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

try:
    thread3 = threading.Thread(target=get_dis)
    thread1 = threading.Thread(target=run_program1)
    thread2 = threading.Thread(target=run_program2)

    thread3.start()
    thread1.start()
    thread2.start()

    thread3.join()
    thread1.join()
    thread2.join()
except KeyboardInterrupt:
    stop_program = True
    thread3.join()
    thread1.join()
    thread2.join()
    cv2.destroyAllWindows()
    GPIO.cleanup()
