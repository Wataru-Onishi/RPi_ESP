#include <WiFi.h>

void setup() {
  Serial.begin(115200); // シリアル通信の開始
  // その他のセットアップコードがあればここに記述
}

void loop() {
  static bool startLogging = false; // ログを開始するかどうかのフラグ

  // シリアルモニタからの入力があるかチェック
  while (Serial.available() > 0) {
    char receivedChar = Serial.read(); // 入力を1文字読み取る
    if (receivedChar == '1') {
      startLogging = true; // データの表示を開始
      Serial.println("Logging started...");
    } else if (receivedChar == '2') {
      startLogging = false; // データの表示を停止
      Serial.println("Logging stopped.");
    }
  }

  // ログ記録が開始された場合の処理
  if (startLogging) {
    // 34番ピンからアナログ値を読み取る（センサーによってはここのコードを適切に変更する必要があります）
    int sensorValue = analogRead(34);
    // ESP32のADCは0〜4095の値を返すため、それを電圧（V）に変換（例：3.3Vを基準とする）
    float voltage = sensorValue * (3.3 / 4095.0);
    // 電圧から圧力(pa)に変換（変換式はセンサーに応じて適切に設定）
    float pressure = (voltage - 1.0) * (850.0 / 1.5); // ここでの変換式は例です

    // 圧力値をシリアルモニタに出力
    Serial.println(pressure);

    // 0.1秒待機（次のデータ読み取りまで）
    delay(100);
  }
}
