#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,16,2); 

void setup() {
  // Open serial communications and wait for port to open:
  lcd.init();                      // initialize the lcd 
  // Print a message to the LCD.
  lcd.backlight();  
  Serial.begin(9600);

}
void loop() { // run over and over
  if (Serial.available()) {
     Serial.write(Serial.read());
     lcd.clear();
     lcd.setCursor(0,0);
     lcd.print(Serial.read());
    }
}
