import serial
import requests

SERIAL_PORT = '/dev/ttyESP32'  # ESP32が接続されているシリアルポート
SERIAL_BAUDRATE = 57600
WEB_APP_URL = 'https://script.google.com/macros/library/d/1Th6OGaTeocE4g-yYgWpgB-SKMWMVg3O0lX6kSxq3Eldf8KwrWni-Za0z/1'  # GASウェブアプリケーションのURL

ser = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=1)

while True:
    if ser.in_waiting >= 4:
        data = ser.read(4)
        pressure_int = int.from_bytes(data, byteorder='big')
        pressure = pressure_int / 1000.0  # kPa単位に変換
        print(f"Pressure: {pressure} kPa")
        
        # Googleスプレッドシートに記録
        response = requests.post(WEB_APP_URL, json={'pressure': pressure})
        print(response.text)
