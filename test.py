import serial
from dynamixel_sdk import *  # Dynamixel SDKライブラリをインポート

# Dynamixel設定
ADDR_TORQUE_ENABLE = 64      # トルク有効化のアドレス
ADDR_OPERATING_MODE = 11     # 動作モード設定のアドレス
ADDR_GOAL_VELOCITY = 104     # 目標速度のアドレス
OPERATING_MODE_VELOCITY = 1  # 速度制御モード
DXL_IDS = [1, 2, 3, 4]       # モータのIDリスト
PROTOCOL_VERSION = 2.0       # 使用するプロトコルバージョン
DEVICENAME = '/dev/DYNAMIXEL' # Dynamixelが接続されたデバイス名
BAUDRATE = 57600             # ボーレート

# ポートの初期化
portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    quit()

if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    quit()

# モータの初期設定を実行
def setup_motors():
    for dxl_id in DXL_IDS:
        # トルクを無効化
        packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, 0)
        # 動作モードを速度制御モードに設定
        packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_OPERATING_MODE, OPERATING_MODE_VELOCITY)
        # トルクを有効化
        packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, 1)

setup_motors()

# シリアル通信設定
ser = serial.Serial('/dev/ESP32', 57600)  # ESP32接続ポートを適宜変更

def motor_control(command):
    # コマンドの形式は "ID:Speed" です
    if ':' in command:
        dxl_id, speed = command.split(':')
        dxl_id = int(dxl_id)
        speed = int(speed)
        
        if dxl_id in DXL_IDS:
            # 指定されたモータIDに対して速度を設定
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, dxl_id, ADDR_GOAL_VELOCITY, speed)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("Invalid motor ID")
    else:
        print("Invalid command format")

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        motor_control(line)
