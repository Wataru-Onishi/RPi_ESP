#include <PS4Controller.h>
#include "Ultrasonic.h"
#include <Arduino.h>

bool mode = true; // true: モード1 (手動), false: モード2 (自動)
Ultrasonic ultrasonic(32); // 超音波センサの入力GPIOを32に設定

void setup() {
  Serial.begin(57600);
  PS4.begin("08:B6:1F:ED:80:36");
  Serial.println("Ready.");

  // ADCの解像度を12ビットに設定
  analogReadResolution(12);


}

void loop() {
  long rangeInCentimeters = ultrasonic.MeasureInCentimeters(); // 超音波センサからの距離を測定
  delay(10);

  if (PS4.Cross()){ // いつでもCrossボタンで全モータ停止
    sendStopCommandToAllMotors();
    return;
  }

  checkModeSwitch();

  if (mode) { // モード1: 手動操作
    manualOperation(rangeInCentimeters);
  } else { // モード2: 自動操作
    autoOperation(rangeInCentimeters);
  }

  // GPIO34からのアナログ値を読み取る（ESP32の場合、ArduinoスタイルでanalogReadを使用）
  int adcValue = analogRead(34);  // GPIO34のピン番号を直接指定
  float voltage = adcValue * (3.3 / 4095.0);  // 12ビット解像度での電圧計算

  // 電圧値をシリアル経由で送信
  Serial.print("Voltage on GPIO34: ");
  Serial.println(voltage, 3);  // 小数点以下3桁で表示

  delay(100);  // 0.1秒間隔でサンプリング

}

void checkModeSwitch() {
  if (PS4.L1()){
    mode = !mode; // モードを切り替える
    Serial.println(mode ? "Manual mode" : "Auto mode");
    sendStopCommandToAllMotors(); // モード切り替え時に全モータ停止
    delay(500); // モード切り替えのデバウンス防止
  }
}


void manualOperation(long rangeInCentimeters) {
  if (rangeInCentimeters <= 5) { // 障害物を検出したら停止
    sendStopCommandToAllMotors();
  } else {
    if (PS4.Up()) {
      // 上ボタンが押された場合、モータ1と2は-100、モータ3と4は100で回転
      Serial.println("1:-100");
      Serial.println("2:-100");
      Serial.println("3:100");
      Serial.println("4:100");
    }
    else if (PS4.Down()) {
      // 下ボタンが押された場合、モータ1と2は100、モータ3と4は-100で回転
      Serial.println("1:100");
      Serial.println("2:100");
      Serial.println("3:-100");
      Serial.println("4:-100");
    }
    delay(100); // コマンド送信後の短い遅延
  }
}

void sendStopCommandToAllMotors() {
  // 全モータを停止
  Serial.println("1:0");
  Serial.println("2:0");
  Serial.println("3:0");
  Serial.println("4:0");
  delay(100); // コマンド送信後の短い遅延
}

void autoOperation(long rangeInCentimeters) {
  static bool isObstacleDetected = false;

  if (PS4.R1()) {
    isObstacleDetected = false; // 障害物検出フラグをリセット
    // R1ボタンで前進（モータ1と2は-100、モータ3と4は100で回転）
    Serial.println("1:-100");
    Serial.println("2:-100");
    Serial.println("3:100");
    Serial.println("4:100");
  }

  if (rangeInCentimeters <= 5 && !isObstacleDetected) {
    isObstacleDetected = true;
    // 障害物を検出した場合、後進（モータ1と2は100、モータ3と4は-100で回転）
    Serial.println("1:100");
    Serial.println("2:100");
    Serial.println("3:-100");
    Serial.println("4:-100");
  }
  delay(100); // コマンド送信後の短い遅延
}
