#include <Arduino.h>
#include <PS4Controller.h>
#include "Ultrasonic.h"

const int adcPin = 34; // ADC入力用ピン

void setup() {
  Serial.begin(57600); // シリアル通信の開始
  PS4.begin("08:B6:1F:ED:80:36");
  analogReadResolution(12); // ADCの解像度を12ビットに設定
  Serial.println("Ready.");
}

void loop() {
  long RangeInCentimeters = ultrasonic.MeasureInCentimeters(); // 超音波センサからの距離を測定
  delay(10);

  if (PS4.Cross()) {
    Serial.println("Cross Button - Stopping");
    Serial.write('0');
    delay(100);
    return;
  }

  checkModeSwitch();

  if (mode) { // モード1: 手動操作
    manualOperation(RangeInCentimeters);
  } else { // モード2: 自動操作
    autoOperation(RangeInCentimeters);
  }
  
  sendVoltageData();
}

void sendVoltageData() {
  int adcValue = analogRead(adcPin); // ADCから値を読み取る
  
  byte adcBytes[2];
  adcBytes[0] = (adcValue >> 8) & 0xFF;
  adcBytes[1] = adcValue & 0xFF;
  
  Serial.write(adcBytes, sizeof(adcBytes)); // ラズベリーパイへ送信
}
