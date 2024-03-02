#include <PS4Controller.h>



void setup() {
  Serial.begin(57600);
  PS4.begin("08:B6:1F:ED:80:36");
  Serial.println("Ready.");

}

void loop() {
    while(true){
      if (PS4.Square()){ 
        Serial.println("Square Button");
        Serial.write("0");
        delay(1000);
      }
      if (PS4.Cross()){
        Serial.println("Cross Button");
        Serial.write("1");
        delay(1000);
      }
      if (PS4.Circle()) Serial.println("Circle Button");
      if (PS4.Triangle()) Serial.println("Triangle Button");




  }


}
