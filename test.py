import time
from dynamixel_sdk import *  # Dynamixel SDKのインポート

# Dynamixelモーターの設定
DXL1_ID = 2  # モーターID2
DXL2_ID = 3  # モーターID3
ADDR_MX_MOVING_SPEED = 104  # MXシリーズの場合の速度制御アドレス
ADDR_XL_TORQUE_ENABLE = 64  # XL430のトルク有効化アドレス
TORQUE_ENABLE = 1  # トルクを有効化する値
BAUDRATE = 57600  # ボーレート
DEVICENAME = '/dev/ttyUSB0'  # ポート名（Windowsでは'COM1', Linuxでは'/dev/ttyUSB0'など）

# Dynamixel SDKの設定
portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(2.0)  # バージョンに応じて変更

# ポートを開く
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    quit()

# ボーレートを設定
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    quit()



# トルクを有効化
packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_XL_TORQUE_ENABLE, TORQUE_ENABLE)
packetHandler.write1ByteTxRx(portHandler, DXL2_ID, ADDR_XL_TORQUE_ENABLE, TORQUE_ENABLE)


# モーターを動かす（ここで速度や回転方向を設定）
DXL_MOVING_SPEED = 100  # 例としての速度値
packetHandler.write2ByteTxRx(portHandler, DXL1_ID, ADDR_MX_MOVING_SPEED, DXL_MOVING_SPEED)
packetHandler.write2ByteTxRx(portHandler, DXL2_ID, ADDR_MX_MOVING_SPEED, DXL_MOVING_SPEED)

# 30秒間待つ
time.sleep(5)

# モーターを停止
packetHandler.write2ByteTxRx(portHandler, DXL1_ID, ADDR_MX_MOVING_SPEED, 0)
packetHandler.write2ByteTxRx(portHandler, DXL2_ID, ADDR_MX_MOVING_SPEED, 0)

# ポートを閉じる
portHandler.closePort()