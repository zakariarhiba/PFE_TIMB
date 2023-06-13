#include <SoftwareSerial.h>
#define outputpin A0
int analogValue = analogRead(outputpin);
float millivolts = (analogValue / 1024.0) * 3300; // 3300 is the voltage provided by NodeMCU
float celsius = millivolts / 10;

String str;

void setup(){
Serial.begin(115200);
Serial1.begin(9600);
delay(2000);
}

void loop()
{
analogValue = analogRead(outputpin);
    millivolts = (analogValue / 1024.0) * 3300; // 3300 is the voltage provided by NodeMCU
    celsius = millivolts / 10;
str =String("Temp= ")+String(10);
Serial1.println(str);

delay(1000);
}
