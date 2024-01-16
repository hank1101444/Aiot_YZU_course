import os
import cv2
import numpy as np
import pwm_motor as motor
import time
import ultrasound
import RPi.GPIO as GPIO
import threading
import logging
# 日志文件的路径
log_file = 'test.log'
if os.path.exists(log_file):
    os.remove(log_file)
logging.basicConfig(level=logging.INFO, filename=log_file,format='%(asctime)s - %(levelname)s - %(message)s')



# 定义一个标志来控制主程序
stop_program = False
left, right, mid = 9999, 9999, 9999
lock = threading.Lock()  # 新增一个锁
sensor1 = ultrasound.UltrasonicSensor(31, 33)  # 左超声波传感器 trig 和 echo 引脚
sensor2 = ultrasound.UltrasonicSensor(22, 36)  # 中间超声波传感器 trig 和 echo 引脚
sensor3 = ultrasound.UltrasonicSensor(7, 15)   # 右超声波传感器 trig 和 echo 引脚


def get_dis():
    global left, right, mid
    global stop_program
    while not stop_program:
        with lock:
            left = sensor1.get_distance()
            mid = sensor2.get_distance()
            right = sensor3.get_distance()
        time.sleep(0.2)  # give time to modify the car pretend dead lock!


def run_program1():
    global stop_program
    try:
        logging.info("Starting run_program1")
        while not stop_program:
            logging.info("start")
            with lock:
                left_, mid_, right_ = left, mid, right
            logging.info(f"Sensor readings - Left: {left_}, Mid: {mid_}, Right: {right_}")

            motor.forward(0.3)
            if left_ < 10 or left_ > 3000:
                logging.info('modify -> left')
                motor.backward(0.2)
                motor.modify_turnRight()

            elif right_ < 10 or right_ > 3000:
                logging.info('modify -> right')
                motor.backward(0.2)
                motor.modify_turnLeft()

            elif mid_ < 20 or mid_ > 3000:
                    motor.stop()
                    logging.info('Obstacle in the middle, stopping and moving backward')
                    motor.backward(0.2)

                    current_left_mid = 0
                    current_right_mid = 0

                    motor.turnLeft(0.7)
                    time.sleep(1)
                    with lock:
                        mid_ = mid
                    current_left_mid = mid_
                    logging.info(f"Distance after turning left: {current_left_mid}")
                    #motor.stop()
                    motor.turnRight(1.4)
                    time.sleep(1)
                    with lock:
                        mid_ = mid
                    current_right_mid = mid_
                    logging.info(f"Distance after turning right: {current_right_mid}")

                    if current_left_mid > current_right_mid:
                        motor.turnLeft(1.3)
                        logging.info("Turning left as it has more space")
            
            #logging.info("in sleep")           
            time.sleep(0.1)  #stock fuck
            #logging.info("out sleep")        

    except Exception as e:
        logging.error(f'run_program1 error: {e}')
        print('run_program1 error')
        motor.cleanup()
        sensor1.cleanup()
        sensor2.cleanup()
        sensor3.cleanup()
    finally:
        logging.info('run_program1 done')
        motor.cleanup()
        sensor1.cleanup()
        sensor2.cleanup()
        sensor3.cleanup()


def run_program2():
    global stop_program
    try:
        # 載入模型和設定
        model_path = "./frozen_inference_graph.xml"
        pbtxt_path = "./frozen_inference_graph.bin"

        net = cv2.dnn.readNet(model_path, pbtxt_path)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)

        # 初始化攝像頭
        cap = cv2.VideoCapture(0, cv2.CAP_V4L)

        # FPS 計算相關變數
        fps_avg_frame_count = 10  # 每 10 幀計算一次 FPS
        counter = 0
        start_time = time.time()
        fps = 0  # 初始化 FPS 值

        if not cap.isOpened():
            raise Exception("无法打开摄像头")

        while not stop_program:
            ret, frame = cap.read()
            if not ret:
                print("无法接收画面 (摄像头结束?). 退出...")
                break
            # 調整幀大小
            img = cv2.resize(frame, (320, 240))
            frame = img.copy()

            # 進行人臉檢測
            blob = cv2.dnn.blobFromImage(
                frame, size=(320, 240), ddepth=cv2.CV_8U)
            net.setInput(blob)
            out = net.forward()

            # 繪製檢測到的人臉
            for detection in out.reshape(-1, 7):
                confidence = float(detection[2])
                xmin = int(detection[3] * frame.shape[1])
                ymin = int(detection[4] * frame.shape[0])
                xmax = int(detection[5] * frame.shape[1])
                ymax = int(detection[6] * frame.shape[0])

                if confidence > 0.5:
                    cv2.rectangle(frame, (xmin, ymin),
                                  (xmax, ymax), color=(0, 255, 0))
                    if detection[1] == 1:
                        cv2.putText(frame, "left", (xmin, ymin - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    elif detection[1] == 2:
                        cv2.putText(frame, "right", (xmin, ymin - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    elif detection[1] == 3:
                        cv2.putText(frame, "stop", (xmin, ymin - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    else:
                        cv2.putText(frame, "duck", (xmin, ymin - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            # 更新計數器並計算 FPS
            counter += 1
            if counter % fps_avg_frame_count == 0:
                end_time = time.time()
                fps = fps_avg_frame_count / (end_time - start_time)
                start_time = time.time()  # 重置計時器
                counter = 0  # 重置計數器

            # 每幀都顯示 FPS
            cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow('live', frame)

            if cv2.waitKey(1) == ord('q'):
                break
    finally:
        print('run_program2 done')
        cap.release()
        cv2.destroyAllWindows()


try:
    thread3 = threading.Thread(target=get_dis)
    thread1 = threading.Thread(target=run_program1)
    thread2 = threading.Thread(target=run_program2)

    thread3.start()
    time.sleep(2)
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
