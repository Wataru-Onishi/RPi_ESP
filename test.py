import requests
import serial
from dynamixel_sdk import *  # Uses Dynamixel SDK library

# シリアルポートとDynamixel設定
SERIAL_PORT = '/dev/ESP32'
SERIAL_BAUDRATE = 57600
WEB_APP_URL = 'https://script.google.com/macros/s/AKfycbyIhj1uDTmSvbPmQ6ENp0EJpskFnE6PZjnF4wfCATjyejfiwTTEppCKn2IMJf47CjSsDg/exec'
ADDR_TORQUE_ENABLE = 64
ADDR_OPERATING_MODE = 11
ADDR_GOAL_VELOCITY = 104
OPERATING_MODE_VELOCITY = 1
DEVICENAME = '/dev/DYNAMIXEL'
PROTOCOL_VERSION = 2.0
BAUDRATE = 57600

# Dynamixelの初期化
dxl_portHandler = PortHandler(DEVICENAME)
dxl_packetHandler = PacketHandler(PROTOCOL_VERSION)
dxl_base_speeds = {1: -100, 2: -100, 3: 100, 4: 100}

if dxl_portHandler.openPort():
    print("Dynamixel port opened successfully")
else:
    print("Failed to open the Dynamixel port")
    quit()

if not dxl_portHandler.setBaudRate(BAUDRATE):
    print("Failed to change the Dynamixel baudrate")
    quit()

# ESP32からのデータ受信用シリアルポートの初期化
ser = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=1)
print("Serial port opened for commands")

def read_pressure_data():
    if ser.in_waiting >= 4:  # 4バイトのデータが利用可能か確認
        pressure_bytes = ser.read(4)  # 4バイト読み取り
        pressure_int = int.from_bytes(pressure_bytes, byteorder='big')
        pressure = pressure_int / 1000.0  # kPa単位に変換
        return pressure
    return None

while True:
    pressure = read_pressure_data()
    if pressure is not None:
        print(f"Pressure: {pressure} kPa")
        # Googleスプレッドシートにデータを送信
        response = requests.post(WEB_APP_URL, json={'pressure': pressure})
        print(response.text)

    if ser.in_waiting > 0:
        command = ser.read().decode('utf-8').strip()
        if command == '0':  # 停止コマンド
            # Dynamixelモーターを停止させるコードをここに記述
            pass
        elif command == '1':  # 前進コマンド
            # Dynamixelモーターを前進させるコードをここに記述
            pass
        elif command == '2':  # 後退コマンド
            # Dynamixelモーターを後退させるコードをここに記述
            pass
