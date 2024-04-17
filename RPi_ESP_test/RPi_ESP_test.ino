#include <PS4Controller.h>

bool isReversing = false; // 後進中かどうかを示すフラグ
bool isForwarding = false; // 前進中かどうかを示すフラグ


void setup() {
  Serial.begin(57600);
  PS4.begin("08:B6:1F:ED:80:36");
  Serial.println("Ready.");
}

void loop() {

  // いつでもCrossボタンで停止
  if (PS4.Cross()){
    Serial.println("Cross Button - Stopping");
    Serial.write('0');
    isReversing = false; // 後進フラグをリセット
    isForwarding = false; // 前進フラグをリセット
    delay(100);
    return;
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

