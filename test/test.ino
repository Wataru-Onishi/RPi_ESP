#include <PS4Controller.h>
#include "Ultrasonic.h"

bool mode = true; // true: モード1 (手動), false: モード2 (自動)
Ultrasonic ultrasonic(32); // 超音波センサの入力GPIOを32に設定

void setup() {
  Serial.begin(57600);
  PS4.begin("08:B6:1F:ED:80:36");
  Serial.println("Ready.");
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
}

void checkModeSwitch() {
  if (PS4.L1()){
    mode = !mode; // モードを切り替える
    Serial.println(mode ? "Manual mode" : "Auto mode");
    sendStopCommandToAllMotors(); // モード切り替え時に全モータ停止
    delay(500); // モード切り替えのデバウンス防止
  }
}

void sendStopCommandToAllMotors() {
  for(int id=1; id<=4; id++){
    Serial.println(String(id) + ":0"); // 各モータを停止
  }
  delay(100);
}

void manualOperation(long rangeInCentimeters) {
  if (rangeInCentimeters <= 5){ // 障害物を検出したら停止
    sendStopCommandToAllMotors();
  } else {
    if (PS4.Up()){
      Serial.println("1:100");
      Serial.println("2:100");
      // モータ3と4を後進させる (速度-100)
      Serial.println("3:-100");
      Serial.println("4:-100");
    }
    else if (PS4.Down()){
      Serial.println("1:-100");
      Serial.println("2:-100");
      // モータ3と4を後進させる (速度-100)
      Serial.println("3:-100");
      Serial.println("4:100");
    }
  }
}

void autoOperation(long rangeInCentimeters) {
  static bool isObstacleDetected = false;

  if (PS4.R1()){
    isObstacleDetected = false; // 障害物検出フラグをリセット
    sendCommandToAllMotors("100"); // 全モータを前進させる
  }

  if (rangeInCentimeters <= 5 && !isObstacleDetected) {
    isObstacleDetected = true;
    sendCommandToAllMotors("-100"); // 障害物を検出したら全モータを後進させる
  }
}

void sendCommandToAllMotors(String speed) {
  for(int id=1; id<=4; id++){
    Serial.println(String(id) + ":" + speed); // 指定した速度で各モータにコマンドを送信
  }
  delay(100);
}
