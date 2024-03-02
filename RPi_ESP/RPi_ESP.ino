#include <PS4Controller.h>



void setup() {
  Serial.begin(57600);
  PS4.begin("08:B6:1F:ED:80:36");
  Serial.println("Ready.");

}

void loop() {
    // while(true){
    //   if (PS4.Up()){ 
    //     Serial.println("Up Button");
    //     Serial.write("0");
    //     delay(100);
    //   }
    //   if (PS4.Cross()){
    //     Serial.println("Cross Button");
    //     Serial.write("1");
    //     delay(100);
    //   }

    while(true){
      if (PS4.Up()){ 
        Serial.println("Up Button");
        Serial.write("0,100");
        Serial.write("1,100");
        delay(100);
      }
      if (PS4.Cross()){
        Serial.println("Cross Button");
        Serial.write("0,0");
        Serial.write("1,0");
        delay(100);
      }



  }


}
