# import RPi.GPIO as GPIO
# import time


# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BOARD)  # 使用物理引脚编号

# # 更新 TRIG 和 ECHO 引脚的编号为物理引脚编号
# # 假设物理引脚 7 对应 BCM 引脚 4，物理引脚 15 对应 BCM 引脚 22
# # 请根据您的实际连接更改这些编号
# TRIG = 7
# ECHO = 15


# GPIO.setup(TRIG, GPIO.OUT)
# GPIO.setup(ECHO, GPIO.IN)


# def get_distance():

#     GPIO.output(TRIG, GPIO.HIGH)
#     time.sleep(2)
#     GPIO.output(TRIG, GPIO.LOW)

#     while GPIO.input(ECHO) == 0:
#         start = time.time()

#     while GPIO.input(ECHO) == 1:
#         end = time.time()

#     D = (end - start) * 17150
#     return D

# if __name__ == "__main__":
#     try:

#         while True:
#             print("{}{:.1f}{}".format("量測距離為: ", get_distance(), "公分"))
#     except KeyboardInterrupt:
#         GPIO.cleanup()

import RPi.GPIO as GPIO
import time

class UltrasonicSensor:
    def __init__(self, trig_pin, echo_pin):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)  # 使用物理引脚编号

        # 设置 GPIO 引脚
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def get_distance(self):
        GPIO.output(self.trig_pin, GPIO.HIGH)
        time.sleep(0.03) #modify
        GPIO.output(self.trig_pin, GPIO.LOW)
        while GPIO.input(self.echo_pin) == 0:
            start = time.time()

        while GPIO.input(self.echo_pin) == 1:
            end = time.time()

        distance = (end - start) * 17150
        return distance

    def cleanup(self):
        GPIO.cleanup()

# 主程序
if __name__ == "__main__":
    try:
        # 创建 UltrasonicSensor 类的实例
        sensor1 = UltrasonicSensor(7, 15)  # 示例引脚号
        sensor2 = UltrasonicSensor(11, 13) # 示例引脚号
        sensor3 = UltrasonicSensor(16, 18) # 示例引脚号

        while True:
            distance1 = sensor1.get_distance()
            print(f"Sensor 1 距离: {distance1:.1f} 公分")
            # 同样可以为 sensor2 和 sensor3 获取距离
            # ...

    except KeyboardInterrupt:
        sensor1.cleanup()
        # 如果需要，也可以为其他传感器调用 cleanup
        # sensor2.cleanup()
        # sensor3.cleanup()
