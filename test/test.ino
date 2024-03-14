#include <PS4Controller.h>
#include "Ultrasonic.h"

bool mode = true; // true: モード1 (手動), false: モード2 (自動)
Ultrasonic frontUltrasonic(32); // 前面の超音波センサの入力GPIOを32に設定
Ultrasonic rearUltrasonic(33); // 後ろの超音波センサの入力GPIOを33に設定

void setup() {
  Serial.begin(57600);
  PS4.begin("08:B6:1F:ED:80:36");
  Serial.println("Ready.");
}

void loop() {
  long frontRange = frontUltrasonic.MeasureInCentimeters(); // 前面の超音波センサからの距離を測定
  long rearRange = rearUltrasonic.MeasureInCentimeters(); // 後ろの超音波センサからの距離を測定
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
    manualOperation(frontRange, rearRange);
  } else { // モード2: 自動操作
    autoOperation(frontRange, rearRange);
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

void manualOperation(long frontRange, long rearRange) {
  if (frontRange <= 5){ // 前方に障害物を検出したら停止
    Serial.println("Obstacle detected in front - Stopping");
    Serial.write('0');
    delay(100);
  } else if (rearRange <= 5 && PS4.Down()){ // 後ろに障害物を検出している間は後進不可
    Serial.println("Obstacle detected in rear - Stopping reverse");
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

void autoOperation(long frontRange, long rearRange) {
  static bool isObstacleDetected = false;
  static bool isReversing = false; // 後進中フラグを追加

  // R1ボタンで正転開始
  if (PS4.R1()){
    isObstacleDetected = false; // 障害物検出フラグをリセット
    isReversing = false; // 後進フラグをリセット
    Serial.println("R1 Button - Starting Forward");
    Serial.write('1');
    delay(100);
  }

  // 前進中に前方のセンサが障害物を検出したら、後進を開始
  if (frontRange <= 5 && !isObstacleDetected && !isReversing) {
    isObstacleDetected = true;
    isReversing = true; // 後進を開始
    Serial.println("Obstacle detected - Reversing");
    Serial.write('2');
    delay(100);
  }

  // 後進中に後ろのセンサが障害物を検出したら、停止
  if (rearRange <= 5 && isReversing) {
    isReversing = false; // 後進を停止
    Serial.println("Obstacle detected in rear - Stopping");
    Serial.write('0');
    delay(100);
  }
}


