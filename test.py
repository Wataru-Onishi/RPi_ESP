import serial
import time

with serial.Serial('/dev/ttyUSB0', 115200, timeout=1) as ser:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            print("Received:", line)
        time.sleep(0.01)
