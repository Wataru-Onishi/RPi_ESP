import time
import serial

# DYNAMIXELの設定
DEVICENAME = '/dev/DYNAMIXEL'  # 接続先のパス
BAUDRATE = 57600  # ボーレート
ID = 7  # DYNAMIXELのID

# コマンド
TORQUE_CONTROL_MODE = 4
VELOCITY_CONTROL_MODE = 1
SET_CURRENT = 1024  # 6mAを表す値
SET_POSITION = 1800

def set_torque_control_mode(port):
    # 電流制御モードに設定
    port.write(bytearray([ID, TORQUE_CONTROL_MODE, 0x00, 0x00]))
    port.flush()

def set_velocity_control_mode(port):
    # 位置制御モードに設定
    port.write(bytearray([ID, VELOCITY_CONTROL_MODE, 0x00, 0x00]))
    port.flush()

def set_current(port, current):
    # 電流制御モードでの電流設定
    port.write(bytearray([ID, 71, current & 0xFF, (current >> 8) & 0xFF]))
    port.flush()

def set_position(port, position):
    # 位置制御モードでの位置設定
    port.write(bytearray([ID, 116, position & 0xFF, (position >> 8) & 0xFF]))
    port.flush()

def main():
    with serial.Serial(DEVICENAME, BAUDRATE) as port:
        port.timeout = 0.1  # タイムアウトを設定
        
        print("DYNAMIXELへの接続完了")
        
        set_torque_control_mode(port)  # 初期は電流制御モード
        
        while True:
            try:
                command = input("1: 電流制御モードで6mA, 2: 位置制御モードで1800, exit: 終了\n")

                if command == "1":
                    set_torque_control_mode(port)
                    set_current(port, SET_CURRENT)
                    print("電流制御モードで6mAを流しました")

                elif command == "2":
                    set_velocity_control_mode(port)
                    set_position(port, SET_POSITION)
                    print("位置制御モードで1800に移動しました")

                elif command == "exit":
                    print("プログラムを終了します")
                    break

                else:
                    print("無効なコマンドです")

            except KeyboardInterrupt:
                print("\nプログラムを終了します")
                break

            time.sleep(0.1)  # ループを速すぎないようにスリープ

if __name__ == "__main__":
    main()
