#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27,16,2);  // set the LCD address to 0x27 for a 16 chars and 2 line display

void setup()
{
  lcd.init();                      // initialize the lcd 
  // Print a message to the LCD.
  lcd.backlight();
  lcd.setCursor(2,0);
  lcd.print("HEALTHCARE");
  lcd.setCursor(4,1);
  lcd.print("CONNECT");
  delay(4000);
  lcd.clear();
    lcd.clear();
 lcd.setCursor(2,0);
  lcd.print("HEALTHCARE");
  lcd.setCursor(0,1);
  lcd.print("Connection     ");
  delay(1000);
  lcd.clear();
 lcd.setCursor(2,0);
  lcd.print("HEALTHCARE");
  lcd.setCursor(0,1);
  lcd.print("Connection .    ");
  delay(1000);
  lcd.clear();
  lcd.setCursor(2,0);
  lcd.print("HEALTHCARE");
  lcd.setCursor(0,1);
  lcd.print("Connection ..    ");
  delay(1000);
  lcd.clear();
  lcd.setCursor(2,0);
  lcd.print("HEALTHCARE");
  lcd.setCursor(0,1);
  lcd.print("Connection ...   ");
  delay(5000);
  lcd.clear();
  lcd.setCursor(3,0);
  lcd.print("HEALTHCARE");
  lcd.setCursor(4,1);
  lcd.print("Connect");
  delay(4000);
  lcd.clear();
}


void loop()
{
   lcd.setCursor(3,0);
  lcd.print("HEALTHCARE");
  lcd.setCursor(4,1);
  lcd.print("CONNECT");
  delay(2000);
   lcd.clear();
  lcd.setCursor(2,0);
  lcd.print("HEALTHCARE");
  lcd.setCursor(4,1);
  lcd.print("READY");
  delay(2000);
  lcd.clear();
 
}
