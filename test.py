import serial
from dynamixel_sdk import *  # Uses Dynamixel SDK library

# シリアルポートの設定
SERIAL_PORT_ESP32 = '/dev/ESP32'  # ESP32が接続されているシリアルポート
SERIAL_BAUDRATE_ESP32 = 57600

# Dynamixelの設定
DEVICENAME_DYNAMIXEL = '/dev/DYNAMIXEL'  # Dynamixelが接続されているシリアルポート
PROTOCOL_VERSION = 2.0
BAUDRATE_DYNAMIXEL = 57600
ADDR_TORQUE_ENABLE = 64
ADDR_OPERATING_MODE = 11
ADDR_GOAL_VELOCITY = 104
OPERATING_MODE_VELOCITY = 1

dxl_portHandler = PortHandler(DEVICENAME_DYNAMIXEL)
dxl_packetHandler = PacketHandler(PROTOCOL_VERSION)

dxl_base_speeds = {
    1: -100,  # モーターID 1の基本速度
    2: -100,  # モーターID 2の基本速度
    3: 100,   # モーターID 3の基本速度
    4: 100    # モーターID 4の基本速度
}

def initialize_dynamixel():
    if dxl_portHandler.openPort():
        print("Dynamixel port opened successfully")
    else:
        print("Failed to open the Dynamixel port")
        quit()

    if not dxl_portHandler.setBaudRate(BAUDRATE_DYNAMIXEL):
        print("Failed to change the Dynamixel baudrate")
        quit()

def control_dynamixel(command):
    if command == '0':  # 停止
        print("Command to stop received")
        for dxl_id in dxl_base_speeds.keys():
            dxl_packetHandler.write4ByteTxRx(dxl_portHandler, dxl_id, ADDR_GOAL_VELOCITY, 0)
            dxl_packetHandler.write1ByteTxRx(dxl_portHandler, dxl_id, ADDR_TORQUE_ENABLE, 0)
    elif command == '1':  # 前進
        print("Command for forward rotation received")
        for dxl_id, speed in dxl_base_speeds.items():
            dxl_packetHandler.write1ByteTxRx(dxl_portHandler, dxl_id, ADDR_OPERATING_MODE, OPERATING_MODE_VELOCITY)
            dxl_packetHandler.write1ByteTxRx(dxl_portHandler, dxl_id, ADDR_TORQUE_ENABLE, 1)
            dxl_packetHandler.write4ByteTxRx(dxl_portHandler, dxl_id, ADDR_GOAL_VELOCITY, speed)
    elif command == '2':  # 後退
        print("Command for reverse rotation received")
        for dxl_id, speed in dxl_base_speeds.items():
            dxl_packetHandler.write1ByteTxRx(dxl_portHandler, dxl_id, ADDR_OPERATING_MODE, OPERATING_MODE_VELOCITY)
            dxl_packetHandler.write1ByteTxRx(dxl_portHandler, dxl_id, ADDR_TORQUE_ENABLE, 1)
            dxl_packetHandler.write4ByteTxRx(dxl_portHandler, dxl_id, ADDR_GOAL_VELOCITY, -speed)

def main():
    ser_esp32 = serial.Serial(SERIAL_PORT_ESP32, SERIAL_BAUDRATE_ESP32, timeout=1)
    print("Serial port for ESP32 opened")
    
    initialize_dynamixel()

    while True:
        if ser_esp32.in_waiting >= 2:
            # ESP32からのコマンドを読み取り、Dynamixelを制御
            command = ser_esp32.read().decode('utf-8').strip()
            control_dynamixel(command)

if __name__ == "__main__":
    main()
