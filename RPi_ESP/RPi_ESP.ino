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
  long RangeInCentimeters = ultrasonic.MeasureInCentimeters(); // 超音波センサからの距離を測定
  delay(10);

  // いつでもCrossボタンで停止
  if (PS4.Cross()){
    Serial.println("Cross Button - Stopping");
    Serial.write('0');
    delay(100);
    return;
  }

  // モード切り替え (L1ボタン) のチェック
  checkModeSwitch();

  if (mode) { // モード1: 手動操作
    manualOperation(RangeInCentimeters);
  } else { // モード2: 自動操作
    autoOperation(RangeInCentimeters);
  }
}

void checkModeSwitch() {
  if (PS4.L1()){
    mode = !mode; // モードを切り替える
    Serial.print("Mode changed to: ");
    Serial.println(mode ? "Manual" : "Auto");
    Serial.write('0'); // モード切り替え時に停止コマンドを送信
    delay(500); // モード切り替えのデバウンス防止
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

  // R1ボタンで正転開始
  if (PS4.R1()){
    isObstacleDetected = false; // 障害物検出フラグをリセット
    Serial.println("R1 Button - Starting Forward");
    Serial.write('1');
    delay(100);
  }

  // 障害物を検出したら逆転開始し続ける
  if (RangeInCentimeters <= 5 && !isObstacleDetected) {
    isObstacleDetected = true;
    Serial.println("Obstacle detected - Reversing");
    Serial.write('2');
    delay(100);
  }
}
