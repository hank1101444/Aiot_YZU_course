import smbus
import time
from enum import Enum
import RPi.GPIO as GPIO
import spidev
import struct

# led
LED_PIN = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN, GPIO.OUT)
pwm = GPIO.PWM(LED_PIN, 100)
pwm.start(0)
brightness = 0



# Get I2C bus
bus = smbus.SMBus(1)
deviceID = bus.read_byte_data(0x53, 0x00)
print("ID: %x" % deviceID)
# ADXL345 address, 0x53(83)
# Select power control register, 0x2D(45)
# 0x08(08) Auto Sleep disable
bus.write_byte_data(0x53, 0x2D, 0x00)
bus.write_byte_data(0x53, 0x2D, 0x08)
# ADXL345 address, 0x53(83)
# Select data format register, 0x31(49)
# 0x08(08) Self test disabled, 4-wire interface
# Full resolution, Range = +/-2g
bus.write_byte_data(0x53, 0x31, 0x08)
time.sleep(0.5)
flag = True
try:
    while True:
        # ADXL345 address, 0x53(83)
        # Read data back from 0x32(50), 2 bytes
        accel = {'x' : 0, 'y' : 0, 'z': 0}
        # X-Axis LSB, X-Axis MSB
        data0 = bus.read_byte_data(0x53, 0x32)
        data1 = bus.read_byte_data(0x53, 0x33)
        # Convert the data to 10-bits
        xAccl = struct.unpack('<h', bytes([data0, data1]))[0]
        accel['x'] = xAccl / 256
        # ADXL345 address, 0x53(83)
        # Read data back from 0x34(52), 2 bytes
        # Y-Axis LSB, Y-Axis MSB
        data0 = bus.read_byte_data(0x53, 0x34)
        data1 = bus.read_byte_data(0x53, 0x35)
        # Convert the data to 10-bits
        yAccl = struct.unpack('<h', bytes([data0, data1]))[0]
        accel['y'] = yAccl / 256
        # ADXL345 address, 0x53(83)
        # Read data back from 0x36(54), 2 bytes
        # Z-Axis LSB, Z-Axis MSB
        data0 = bus.read_byte_data(0x53, 0x36)
        data1 = bus.read_byte_data(0x53, 0x37)
        # Convert the data to 10-bits
        zAccl = struct.unpack('<h', bytes([data0, data1]))[0]
        accel['z'] = zAccl / 256
        # Output data to screen
           # if 45 degree -> bright 50 %
        print ("Ax : %.3f" % (accel['x']))
        if(int(accel['x'] * 100) < 0):
            pwm.ChangeDutyCycle(0)
            flag = not flag
        
        if flag:
            if(int(accel['x'] * 100) < 100 and int(accel['x'] * 100) > 0):
                pwm.ChangeDutyCycle(int(accel['x'] * 100))
        time.sleep(0.1)
        
            
except KeyboardInterrupt:
    print("Ctrl+C Break")
    pwm.stop()
    GPIO.cleanup()
