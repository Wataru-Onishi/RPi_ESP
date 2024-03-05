#include <PS4Controller.h>
#include "Ultrasonic.h"
#include <Arduino.h>

bool mode = true; // true: モード1 (手動), false: モード2 (自動)
Ultrasonic ultrasonic(32); // 超音波センサの入力GPIOを32に設定
const int adcPin = 34; // ADCピン番号
const long interval = 100; // サンプリング間隔（ミリ秒）
const float voltageConversionFactor = 3.3 / 4095.0; // ADCの電圧変換係数

void setup() {
  Serial.begin(57600);
  PS4.begin("08:B6:1F:ED:80:36");
  analogReadResolution(12); // ADCの解像度を12ビットに設定
  Serial.println("Ready.");
}

void loop() {
  static unsigned long lastSampleTime = 0; // 前回のサンプリング時間
  unsigned long currentTime = millis();
  
  if (currentTime - lastSampleTime >= interval) {
    lastSampleTime = currentTime;
    sendPressureData();
  }
  
  long RangeInCentimeters = ultrasonic.MeasureInCentimeters(); // 超音波センサからの距離を測定
  delay(10);

  if (PS4.Cross()){
    Serial.println("Cross Button - Stopping");
    Serial.write('0');
    delay(100);
    return;
  }

  checkModeSwitch();

  if (mode) {
    manualOperation(RangeInCentimeters);
  } else {
    autoOperation(RangeInCentimeters);
  }
}

void sendPressureData() {
  int adcValue = analogRead(adcPin);
  float voltage = adcValue * voltageConversionFactor;
  float pressure;
  // 1V以下の場合、圧力を0とする
  if (voltage <= 1.0) {
    pressure = 0;
  } else {
    // 圧力の計算
    pressure = (voltage - 1.0) * (0.81 / (2.6 - 1.0));
  }
  // 圧力値を1000倍して整数化
  unsigned long pressureInt = static_cast<unsigned long>(pressure * 1000); // 圧力値を1000倍して整数化
  byte pressureBytes[4];
  pressureBytes[0] = (pressureInt >> 24) & 0xFF;
  pressureBytes[1] = (pressureInt >> 16) & 0xFF;
  pressureBytes[2] = (pressureInt >> 8) & 0xFF;
  pressureBytes[3] = pressureInt & 0xFF;
  Serial.write(pressureBytes, sizeof(pressureBytes));
}


void checkModeSwitch() {
  if (PS4.L1()){
    mode = !mode;
    Serial.print("Mode changed to: ");
    Serial.println(mode ? "Manual" : "Auto");
    Serial.write('0');
    delay(500);
  }
}

void manualOperation(long RangeInCentimeters) {
  if (RangeInCentimeters <= 5){ // 障害物を検出したら停止
    Serial.println("Obstacle detected - Stopping");
    Serial.write('0');
    delay(100);
  } else {
    // Upボタンで正転
    if (PS4.Up()){
      Serial.println("Up Button - Forward");
      Serial.write('1');
      delay(100);
    }
    // Downボタンで逆転
    else if (PS4.Down()){
      Serial.println("Down Button - Reverse");
      Serial.write('2');
      delay(100);
    }
  }
}

void autoOperation(long RangeInCentimeters) {
  static bool isObstacleDetected = false;

  if (PS4.R1() && !isObstacleDetected){
    Serial.println("R1 Button - Starting Forward");
    Serial.write('1');
    delay(100);
  }

  if (RangeInCentimeters <= 5 && !isObstacleDetected) {
    isObstacleDetected = true;
    Serial.println("Obstacle detected - Reversing");
    Serial.write('2');
    delay(100);
  }

  // 障害物がなくなった場合、逆転を停止し障害物検出フラグをリセット
  if (!isObstacleDetected || (isObstacleDetected && RangeInCentimeters > 5)) {
    isObstacleDetected = false;
    Serial.println("Path clear - Stopping");
    Serial.write('0');
    delay(100);
  }
}
