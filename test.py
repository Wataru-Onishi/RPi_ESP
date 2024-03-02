from dynamixel_sdk import *                    # Dynamixel SDKのインポート
import time                                    # タイマー機能のためのインポート

# Dynamixelの設定値
DXL_ID = 1                                     # Dynamixel ID
BAUDRATE = 57600                               # Dynamixelのボーレート
DEVICENAME = '/dev/ttyUSB0'                    # ポート名（環境に合わせて変更）
PROTOCOL_VERSION = 2.0                         # 使用するプロトコルバージョン

# XL430-W250のコントロールテーブルアドレス
ADDR_XL430_OPERATING_MODE = 11                 # 動作モードのアドレス
ADDR_XL430_GOAL_VELOCITY = 104                 # 目標速度のアドレス
VELOCITY_CONTROL_MODE = 1                      # 速度制御モード

# サーボモーターの速度設定（範囲：-1023～1023）
DXL_MOVING_SPEED = 200                         # サーボが回転する速度

# ポートの初期化
portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

# ポートのオープン
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    quit()

# ボーレートの設定
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    quit()

# 動作モードの設定（速度制御モード）
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_XL430_OPERATING_MODE, VELOCITY_CONTROL_MODE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Operating mode changed to velocity control mode")

# 目標速度の設定
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_XL430_GOAL_VELOCITY, DXL_MOVING_SPEED)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel has been set to the specified speed")

# 5秒間待機
time.sleep(5)

# サーボの停止
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_XL430_GOAL_VELOCITY, 0)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel has been stopped")

# ポートのクローズ
portHandler.closePort()
