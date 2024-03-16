#include <PS4Controller.h>
#include "Ultrasonic.h"

bool mode = true; // true: モード1 (手動), false: モード2 (自動)
Ultrasonic ultrasonicFront(32); // 前方向の超音波センサの入力GPIOを32に設定
Ultrasonic ultrasonicBack(33); // 後方向の超音波センサの入力GPIOを33に設定
bool isReversing = false; // 後進中かどうかを示すフラグ
bool isForwarding = false; // 前進中かどうかを示すフラグ

// 検出距離の閾値を変数で定義
const long frontObstacleDistance = 5; // 前方の障害物検出距離(センチメートル)
const long backObstacleDistance = 5; // 後方の障害物検出距離(センチメートル)

void setup() {
  Serial.begin(57600);
  PS4.begin("08:B6:1F:ED:80:36");
  Serial.println("Ready.");
}

void loop() {
  long frontRange = ultrasonicFront.MeasureInCentimeters(); // 前方の超音波センサからの距離を測定
  long backRange = ultrasonicBack.MeasureInCentimeters(); // 後方の超音波センサからの距離を測定
  delay(10);

  // いつでもCrossボタンで停止
  if (PS4.Cross()){
    Serial.println("Cross Button - Stopping");
    Serial.write('0');
    isReversing = false; // 後進フラグをリセット
    isForwarding = false; // 前進フラグをリセット
    delay(100);
    return;
  }

  // モード切り替え (L1ボタン) のチェック
  checkModeSwitch();

  if (mode) { // モード1: 手動操作
    manualOperation(frontRange, backRange);
  } else { // モード2: 自動操作
    autoOperation(frontRange, backRange);
  }
}

void checkModeSwitch() {
  if (PS4.L1()){
    mode = !mode; // モードを切り替える
    Serial.print("Mode changed to: ");
    Serial.println(mode ? "Manual" : "Auto");
    Serial.write('0'); // モード切り替え時に停止コマンドを送信
    isReversing = false; // 後進フラグをリセット
    isForwarding = false; // 前進フラグをリセット
    delay(500); // モード切り替えのデバウンス防止
  }
}

void manualOperation(long frontRange, long backRange) {
  // 前方に障害物を検出した場合
  if (frontRange <= frontObstacleDistance) {
    Serial.println("Front obstacle detected - Stopping");
    Serial.write('0'); // 停止コマンドを送信
    delay(1000); // 1秒間停止

    Serial.println("Reversing for 1 second");
    Serial.write('2'); // 後進コマンドを送信
    delay(1000); // 1秒間後進
    Serial.write('0'); // 停止コマンドを送信
    return; // 障害物を検出した場合は、その他の操作を無視
  }

  // 後方に障害物を検出した場合
  if (backRange <= backObstacleDistance) {
    Serial.println("Back obstacle detected - Stopping");
    Serial.write('0'); // 停止コマンドを送信
    delay(1000); // 1秒間停止

    Serial.println("Forwarding for 1 second");
    Serial.write('1'); // 前進コマンドを送信
    delay(1000); // 1秒間前進
    Serial.write('0'); // 停止コマンドを送信
    return; // 障害物を検出した場合は、その他の操作を無視
  }

  // Upボタンで正転（前進）
  if (PS4.Up()){
    Serial.println("Up Button - Forward");
    Serial.write('1');
    delay(100);
  }
  // Downボタンで逆転（後進）
  else if (PS4.Down()){
    Serial.println("Down Button - Reverse");
    Serial.write('2');
    delay(100);
  }
}


void autoOperation(long frontRange, long backRange) {
  // R1ボタンで前進開始
  if (PS4.R1() && !isForwarding && !isReversing){
    isForwarding = true; // 前進フラグをセット
    Serial.println("R1 Button - Starting Forward");
    Serial.write('1');
    delay(100);
  }

  // 前進中に前方のセンサが障害物を検出したら1秒停止後、後進開始
  if (isForwarding && frontRange <= frontObstacleDistance) {
    Serial.println("Obstacle detected - Stopping, then reversing");
    Serial.write('0'); // 停止
    delay(1000); // 1秒停止
    isForwarding = false; // 前進フラグをリセット
    isReversing = true; // 後進フラグをセット
    Serial.println("Reversing");
    Serial.write('2'); // 後進開始
    delay(100);
  }

  // 後進中に後方のセンサが障害物を検出したら停止
  if (isReversing && backRange <= backObstacleDistance) {
    Serial.println("Obstacle detected while reversing - Stopping");
    Serial.write('0'); // 停止
    isReversing = false; // 後進フラグをリセット
    delay(100);
  }
}


void forword(){
  
}