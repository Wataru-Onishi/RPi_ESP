import serial
from dynamixel_sdk import *

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

# ESP32とのシリアル通信設定
esp32_serial = serial.Serial('/dev/ESP32', 57600)

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

try:
    while True:
        # ESP32から電圧値を受信
        voltage_data = esp32_serial.readline().decode().strip()
        
        if voltage_data:
            # 受信した電圧値を表示
            print("Received voltage:", voltage_data)

            # 受信した電圧値に対する処理を追加する場合はここに記述
            # 例: 特定の電圧値に対してモーターの速度を変更するなどのアクションを実行

        time.sleep(0.1)  # 0.1秒間隔で受信

except KeyboardInterrupt:
    # キーボード割り込みが検出された場合、プログラムを終了
    print("Keyboard interrupt detected. Exiting...")
finally:
    # シリアルポートをクローズ
    esp32_serial.close()
    portHandler.closePort()
