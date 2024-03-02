#include <PS4Controller.h>

bool mode = true; // true: モード1 (手動), false: モード2 (自動)

void setup() {
  Serial.begin(57600);
  PS4.begin("08:B6:1F:ED:80:36");
  Serial.println("Ready.");
}

void loop() {
  // モード切り替え (L1ボタン)
  if (PS4.L1()){
    mode = !mode; // モードを切り替える
    Serial.print("Mode changed to: ");
    Serial.println(mode ? "Manual" : "Auto");
    delay(1000); // モード切り替えのデバウンス防止
  }
  
  if (mode) { // モード1: 手動操作
    if (PS4.Cross()){ 
      Serial.println("Cross Button");
      Serial.write('0');
      delay(100);
    }
    if (PS4.Up()){
      Serial.println("Up Button");
      Serial.write('1');
      delay(100);
    }
    if (PS4.Down()){
      Serial.println("Down Button");
      Serial.write('2');
      delay(100);
    }
  } else { // モード2: 自動操作
    // センサー入力に基づくコードをここに挿入
    // 例: Serial.write('1'); // センサー入力に基づいた何らかの条件下で
    // delay(1000); // センサーからのデータ処理に適した遅延
  }
}
