#include <PS4Controller.h>
#include "Ultrasonic.h"

bool mode = true; // true: モード1 (手動), false: モード2 (自動)
Ultrasonic ultrasonicFront(32); // 前方向の超音波センサの入力GPIOを32に設定
Ultrasonic ultrasonicBack(33); // 後方向の超音波センサの入力GPIOを33に設定

// 検出距離の閾値を変数で定義
const long frontObstacleDistance = 5; // 前方の障害物検出距離(センチメートル)
const long backObstacleDistance = 5; // 後方の障害物検出距離(センチメートル)

bool isReversing = false; // 後進中かどうかを示すフラグ
bool isForwarding = false; // 前進中かどうかを示すフラグ

void setup() {
  Serial.begin(57600);
  PS4.begin("08:B6:1F:ED:80:36");
  Serial.println("Ready.");
}

void loop() {
  long frontRange = ultrasonicFront.MeasureInCentimeters(); // 前方の超音波センサからの距離を測定
  long backRange = ultrasonicBack.MeasureInCentimeters(); // 後方の超音波センサからの距離を測定
  delay(10);

  if (PS4.Cross()){
    Serial.println("Cross Button - Stopping");
    sendMotorSpeeds(0, 0, 0, 0); // すべてのモータを停止
    delay(100);
    return;
  }

  checkModeSwitch();

  if (mode) { // モード1: 手動操作
    manualOperation(frontRange, backRange);
  } else { // モード2: 自動操作
    autoOperation(frontRange, backRange);
  }
}

void sendMotorSpeeds(int m1Speed, int m2Speed, int m3Speed, int m4Speed) {
  Serial.print(String(m1Speed) + "," + String(m2Speed) + "," + String(m3Speed) + "," + String(m4Speed) + "\n");
}

void checkModeSwitch() {
  static unsigned long lastPressTime = 0;
  unsigned long currentTime = millis();

  // L1ボタンでモード切り替え
  if (PS4.L1() && currentTime - lastPressTime > 500) { // デバウンス対策として500msの間隔を設定
    mode = !mode; // モードを切り替える
    Serial.print("Mode changed to: ");
    Serial.println(mode ? "Manual" : "Auto");
    
    // モード切り替え時に全てのモータを停止させる命令を送信
    sendMotorSpeeds(0, 0, 0, 0);

    lastPressTime = currentTime; // 最後にボタンが押された時間を更新
    delay(500); // モード切り替えのデバウンス防止のための遅延
  }
}


void manualOperation(long frontRange, long backRange) {
  // 前方に障害物を検出した場合、後進する
  if (frontRange <= frontObstacleDistance) {
    Serial.println("Front obstacle detected - Reversing");
    sendMotorSpeeds(-200, -200, -200, -200); // すべてのモータを後進スピードで動作
    delay(1000); // 1秒間後進
    sendMotorSpeeds(0, 0, 0, 0); // 停止
  }
  // 後方に障害物を検出した場合、前進する
  else if (backRange <= backObstacleDistance) {
    Serial.println("Back obstacle detected - Forwarding");
    sendMotorSpeeds(200, 200, 200, 200); // すべてのモータを前進スピードで動作
    delay(1000); // 1秒間前進
    sendMotorSpeeds(0, 0, 0, 0); // 停止
  }
  // PS4コントローラのUpボタンで前進
  else if (PS4.Up()){
    Serial.println("Up Button - Forward");
    sendMotorSpeeds(200, 200, 200, 200); // すべてのモータを前進スピードで動作
  }
  // PS4コントローラのDownボタンで後進
  else if (PS4.Down()){
    Serial.println("Down Button - Reverse");
    sendMotorSpeeds(-200, -200, -200, -200); // すべてのモータを後進スピードで動作
  }
  // その他の場合は停止
  else {
    sendMotorSpeeds(0, 0, 0, 0); // すべてのモータを停止
  }
}


void autoOperation(long frontRange, long backRange) {
  if (frontRange <= frontObstacleDistance && !isReversing) {
    Serial.println("Obstacle detected - Stopping, then reversing");
    sendMotorSpeeds(0, 0, 0, 0); // 停止
    delay(1000); // 1秒停止
    isReversing = true; // 後進フラグをセット
    Serial.println("Reversing");
    sendMotorSpeeds(-200, -200, -200, -200); // すべてのモータを後進スピードで動作
  } else if (backRange <= backObstacleDistance && isReversing) {
    Serial.println("Obstacle detected while reversing - Stopping");
    sendMotorSpeeds(0, 0, 0, 0); // 停止
    isReversing = false; // 後進フラグをリセット
  }
  // 前進命令 (R1ボタン)
  if (PS4.R1() && !isForwarding && !isReversing){
    isForwarding = true; // 前進フラグをセット
    Serial.println("R1 Button - Starting Forward");
    sendMotorSpeeds(200, 200, 200, 200); // すべてのモータを前進スピードで動作
  } else if (!PS4.R1() && isForwarding) {
    isForwarding = false; // 前進フラグをリセット
    sendMotorSpeeds(0, 0, 0, 0); // 停止
  }
}


