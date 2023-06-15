#include <Adafruit_MAX31865.h>

// Use software SPI: CS, DI, DO, CLK
Adafruit_MAX31865 thermo = Adafruit_MAX31865(D10, D11, D12, D13);
// use hardware SPI, just pass in the CS pin
//Adafruit_MAX31865 thermo = Adafruit_MAX31865(10);

// The value of the Rref resistor. Use 430.0 for PT100 and 4300.0 for PT1000
#define RREF      430.0
// The 'nominal' 0-degrees-C resistance of the sensor
// 100.0 for PT100, 1000.0 for PT1000
#define RNOMINAL  100.0

#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27,16,2);  


#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi
const char *ssid = "moniteur";     // Enter your WiFi name
const char *password = "12345678"; // Enter WiFi password

// MQTT Broker
const char *mqtt_broker = "test.mosquitto.org";
const char *topic = "monitorAlert/CHU";
const char *mqtt_username = "";
const char *mqtt_password = "";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

char msg_out[20];


void setup() {
  lcd.init();                      // initialize the lcd 
  // Print a message to the LCD.
  lcd.backlight();
  lcd.setCursor(3,0);
  lcd.print("HEALTHCARE");
  lcd.setCursor(4,1);
  lcd.print("CONNECT");
  delay(3000);
  Serial.begin(9600);
  


  // connecting to a WiFi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.println("Connecting to WiFi...");
    lcd.clear();
    lcd.setCursor(3,0);
    lcd.print("HEALTHCARE");
    lcd.setCursor(0,1);
    lcd.print("WIFI...");
  }
  Serial.println("Connected to the WiFi network");
  lcd.clear();
    lcd.setCursor(3,0);
    lcd.print("HEALTHCARE");
    lcd.setCursor(0,1);
    lcd.print("WIFI DONE");
  delay(500);
  // connecting to a mqtt broker
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);
  while (!client.connected())
  {
    String client_id = "esp8266-client-";
    client_id += String(WiFi.macAddress());
    Serial.printf("The client %s connects to the public mqtt broker\n", client_id.c_str());
    if (client.connect(client_id.c_str(), mqtt_username, mqtt_password))
    {
      // print message
      Serial.println("Public mosquitoo mqtt broker connected");
      lcd.clear();
    lcd.setCursor(3,0);
    lcd.print("HEALTHCARE");
    lcd.setCursor(0,1);
    lcd.print("MQTT DONE");
    }
    else
    {
      // print message
      Serial.print("failed with state ");
      Serial.print(client.state());
      lcd.clear();
    lcd.setCursor(3,0);
    lcd.print("HEALTHCARE");
    lcd.setCursor(0,1);
    lcd.print("MQTT FAIL");
      delay(2000);
    }
  }

  thermo.begin(MAX31865_3WIRE);  // set to 2WIRE or 4WIRE as necessary
  // publish and subscribe
  client.subscribe(topic);
  delay(2000);

  
}


void loop() {
    uint16_t rtd = thermo.readRTD();
    float ratio = rtd;
    ratio /= 32768;

    float temp = thermo.temperature(RNOMINAL, RREF);
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("HEALTHCARE");
    lcd.setCursor(0,1);
    lcd.print("TEMP : ");
    lcd.setCursor(8,1);
    lcd.print(temp);


    sprintf(msg_out, "%2.f", temp);
    Serial.print("Temp : ");
    Serial.println(msg_out);
    // Publishe the data to the broker
    client.publish("moniteurCHU/patient2/temp", msg_out);


    
    delay(2000);
}


// Function Called when a message arrived
void callback(char *topic, byte *payload, unsigned int length)
{
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  Serial.print("Message:");
  for (int i = 0; i < length; i++)
  {
    Serial.print((char)payload[i]);
  }
  Serial.println();
  Serial.println("-----------------------");
}
