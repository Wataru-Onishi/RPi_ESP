#include <PS4Controller.h>



void setup() {
  Serial.begin(57600);
  PS4.begin("08:B6:1F:ED:80:36");
  Serial.println("Ready.");

}

void loop() {
    while(true){
      if (PS4.Cross()){ 
        Serial.println("Cross Button");
        Serial.write("0");
        delay(100);
      }
      if (PS4.Up()){
        Serial.println("Up Button");
        Serial.write("1");
        delay(100);
      }
      if (PS4.Down()){
        Serial.println("Down Button");
        Serial.write("2");
        delay(100);
      }
  }

}
