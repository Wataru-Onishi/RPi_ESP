#include <Arduino.h>

const int adcPin = 34; // ADC入力用ピン
const float maxVoltage = 3.3; // ESP32のADCの最大電圧
const int adcResolution = 4095; // ADCの分解能 (12ビット)

void setup() {
  Serial.begin(57600); // シリアル通信の開始
  analogReadResolution(12); // ADCの解像度を12ビットに設定
}

void loop() {
  int adcValue = analogRead(adcPin); // ADCから値を読み取る
  float voltage = (adcValue * maxVoltage) / adcResolution; // 読み取った値を電圧に変換
  
  // 電圧を圧力にマッピング
  float pressure = 0;
  if (voltage > 1.0) {
    pressure = (voltage - 1.0) * (810.0 / (2.6 - 1.0));
  }
  
  // 圧力値を整数化してシリアル通信で送信
  unsigned long pressureInt = static_cast<unsigned long>(pressure);
  byte pressureBytes[4];
  pressureBytes[0] = (pressureInt >> 24) & 0xFF;
  pressureBytes[1] = (pressureInt >> 16) & 0xFF;
  pressureBytes[2] = (pressureInt >> 8) & 0xFF;
  pressureBytes[3] = pressureInt & 0xFF;
  
  Serial.write(pressureBytes, sizeof(pressureBytes));
  
  delay(1000); // 1秒ごとにデータを送信
}
