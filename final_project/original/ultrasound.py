import RPi.GPIO as GPIO
import time


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)  # 使用物理引脚编号

# 更新 TRIG 和 ECHO 引脚的编号为物理引脚编号
# 假设物理引脚 7 对应 BCM 引脚 4，物理引脚 15 对应 BCM 引脚 22
# 请根据您的实际连接更改这些编号
TRIG = 7
ECHO = 15


GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)


def get_distance():

    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(TRIG, GPIO.LOW)

    while GPIO.input(ECHO) == 0:
        start = time.time()

    while GPIO.input(ECHO) == 1:
        end = time.time()

    D = (end - start) * 17150
    return D

if __name__ == "__main__":
    try:

        while True:
            print("{}{:.1f}{}".format("量測距離為: ", get_distance(), "公分"))
    except KeyboardInterrupt:
        GPIO.cleanup()
