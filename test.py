import serial

# シリアルポートの設定。デバイス名は環境に合わせて適宜変更してください。
SERIAL_PORT = '/dev/ESP32'
SERIAL_BAUDRATE = 57600

def read_adc_value(ser):
    # 2バイト読み取り
    data = ser.read(2)
    if len(data) == 2:
        # バイトデータを整数値に変換
        adc_value = (data[0] << 8) | data[1]
        return adc_value
    else:
        # データが不完全な場合はNoneを返す
        return None

def main():
    with serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=1) as ser:
        print("Serial port opened for commands")

        while True:
            adc_value = read_adc_value(ser)
            if adc_value is not None:
                print(f"ADC Value: {adc_value}")
                # 必要に応じて電圧値に変換
                voltage = (adc_value * 3.3) / 4095  # ここでの3.3はESP32の参照電圧
                print(f"Voltage: {voltage:.2f} V")

if __name__ == "__main__":
    main()
