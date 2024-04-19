#include <PS4Controller.h>

void setup() {
  Serial.begin(57600);
  if (!PS4.begin("08:B6:1F:ED:80:36")) {
    Serial.println("Failed to initialize PS4 controller");
    while (1);
  }
  Serial.println("PS4 controller is ready");
}

void loop() {
  if (PS4.isConnected()) {
    printControllerData();
  }
  delay(10);
}

void printControllerData() {
  // ボタンの状態を確認
  if (PS4.data.button.square) Serial.println("Square button pressed");
  if (PS4.data.button.cross) Serial.println("Cross button pressed");
  if (PS4.data.button.circle) Serial.println("Circle button pressed");
  if (PS4.data.button.triangle) Serial.println("Triangle button pressed");
  
  if (PS4.data.button.up) Serial.println("Up button pressed");
  if (PS4.data.button.down) Serial.println("Down button pressed");
  if (PS4.data.button.left) Serial.println("Left button pressed");
  if (PS4.data.button.right) Serial.println("Right button pressed");

  if (PS4.data.button.l1) Serial.println("L1 button pressed");
  if (PS4.data.button.r1) Serial.println("R1 button pressed");
  if (PS4.data.button.l2) Serial.println("L2 button pressed");
  if (PS4.data.button.r2) Serial.println("R2 button pressed");

  if (PS4.data.button.share) Serial.println("Share button pressed");
  if (PS4.data.button.options) Serial.println("Options button pressed");
  if (PS4.data.button.l3) Serial.println("L3 button pressed");
  if (PS4.data.button.r3) Serial.println("R3 button pressed");
  if (PS4.data.button.ps) Serial.println("PS button pressed");
  if (PS4.data.button.touchpad) Serial.println("Touchpad button pressed");

  // アナログスティックの値を出力
  Serial.print("Left Stick X: ");
  Serial.println(PS4.data.analog.stick.lx);
  Serial.print("Left Stick Y: ");
  Serial.println(PS4.data.analog.stick.ly);
  
  Serial.print("Right Stick X: ");
  Serial.println(PS4.data.analog.stick.rx);
  Serial.print("Right Stick Y: ");
  Serial.println(PS4.data.analog.stick.ry);
  
  delay(100); // 少し待ち時間を設ける
}
