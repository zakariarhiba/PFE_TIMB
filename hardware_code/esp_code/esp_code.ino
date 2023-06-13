#define NOTE_B0 31
#define NOTE_C1 33
#define NOTE_CS1 35
#define NOTE_D1 37
#define NOTE_DS1 39
#define NOTE_E1 41
#define NOTE_F1 44
#define NOTE_FS1 46
#define NOTE_G1 49
#define NOTE_GS1 52
#define NOTE_A1 55
#define NOTE_AS1 58
#define NOTE_B1 62
#define NOTE_C2 65
#define NOTE_CS2 69
#define NOTE_D2 73
#define NOTE_DS2 78
#define NOTE_E2 82
#define NOTE_F2 87
#define NOTE_FS2 93
#define NOTE_G2 98
#define NOTE_GS2 104
#define NOTE_A2 110
#define NOTE_AS2 117
#define NOTE_B2 123
#define NOTE_C3 131
#define NOTE_CS3 139
#define NOTE_D3 147
#define NOTE_DS3 156
#define NOTE_E3 165
#define NOTE_F3 175
#define NOTE_FS3 185
#define NOTE_G3 196
#define NOTE_GS3 208
#define NOTE_A3 220
#define NOTE_AS3 233
#define NOTE_B3 247
#define NOTE_C4 262
#define NOTE_CS4 277
#define NOTE_D4 294
#define NOTE_DS4 311
#define NOTE_E4 330
#define NOTE_F4 349
#define NOTE_FS4 370
#define NOTE_G4 392
#define NOTE_GS4 415
#define NOTE_A4 440
#define NOTE_AS4 466
#define NOTE_B4 494
#define NOTE_C5 523
#define NOTE_CS5 554
#define NOTE_D5 587
#define NOTE_DS5 622
#define NOTE_E5 659
#define NOTE_F5 698
#define NOTE_FS5 740
#define NOTE_G5 784
#define NOTE_GS5 831
#define NOTE_A5 880
#define NOTE_AS5 932
#define NOTE_B5 988
#define NOTE_C6 1047
#define NOTE_CS6 1109
#define NOTE_D6 1175
#define NOTE_DS6 1245
#define NOTE_E6 1319
#define NOTE_F6 1397
#define NOTE_FS6 1480
#define NOTE_G6 1568
#define NOTE_GS6 1661
#define NOTE_A6 1760
#define NOTE_AS6 1865
#define NOTE_B6 1976
#define NOTE_C7 2093
#define NOTE_CS7 2217
#define NOTE_D7 2349
#define NOTE_DS7 2489
#define NOTE_E7 2637
#define NOTE_F7 2794
#define NOTE_FS7 2960
#define NOTE_G7 3136
#define NOTE_GS7 3322
#define NOTE_A7 3520
#define NOTE_AS7 3729
#define NOTE_B7 3951
#define NOTE_C8 4186
#define NOTE_CS8 4435
#define NOTE_D8 4699
#define NOTE_DS8 4978
#define REST 0

// change this to make the song slower or faster
int tempo = 400;

int buzzer = D5;

// notes of the moledy followed by the duration.
// a 4 means a quarter note, 8 an eighteenth , 16 sixteenth, so on
// !!negative numbers are used to represent dotted notes,
// so -4 means a dotted quarter note, that is, a quarter plus an eighteenth!!
int melody[] = {

    // Silent Night  Buzzer Song, Original Version

    NOTE_G4,
    -4,
    NOTE_A4,
    8,
    NOTE_G4,
    4,
    NOTE_E4,
    -2,
    NOTE_G4,
    -4,
    NOTE_A4,
    8,
    NOTE_G4,
    4,
    NOTE_E4,
    -2,
    NOTE_D5,
    2,
    NOTE_D5,
    4,
    NOTE_B4,
    -2,
    NOTE_C5,
    2,
    NOTE_C5,
    4,
    NOTE_G4,
    -2,

    NOTE_A4,
    2,
    NOTE_A4,
    4,
    NOTE_C5,
    -4,
    NOTE_B4,
    8,
    NOTE_A4,
    4,
    NOTE_G4,
    -4,
    NOTE_A4,
    8,
    NOTE_G4,
    4,
    NOTE_E4,
    -2,
    NOTE_A4,
    2,
    NOTE_A4,
    4,
    NOTE_C5,
    -4,
    NOTE_B4,
    8,
    NOTE_A4,
    4,
    NOTE_G4,
    -4,
    NOTE_A4,
    8,
    NOTE_G4,
    4,
    NOTE_E4,
    -2,

    NOTE_D5,
    2,
    NOTE_D5,
    4,
    NOTE_F5,
    -4,
    NOTE_D5,
    8,
    NOTE_B4,
    4,
    NOTE_C5,
    -2,
    NOTE_E5,
    -2,
    NOTE_C5,
    4,
    NOTE_G4,
    4,
    NOTE_E4,
    4,
    NOTE_G4,
    -4,
    NOTE_F4,
    8,
    NOTE_D4,
    4,
    NOTE_C4,
    -2,
    NOTE_C4,
    -1,
};

// sizeof gives the number of bytes, each int value is composed of two bytes (16 bits)
// there are two values per note (pitch and duration), so for each note there are four bytes
int notes = sizeof(melody) / sizeof(melody[0]) / 2;

// this calculates the duration of a whole note in ms
int wholenote = (60000 * 4) / tempo;

int divider = 0, noteDuration = 0;

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#define outputpin A0
#define ledB D3

#include <Wire.h>
#include "MAX30100_PulseOximeter.h"
#define REPORTING_PERIOD_MS 10000

// Create a PulseOximeter object
PulseOximeter pox;

// Time at which the last beat occurred
uint32_t tsLastReport = 0;

int analogValue = analogRead(outputpin);
float millivolts = (analogValue / 1024.0) * 3300; // 3300 is the voltage provided by NodeMCU
float celsius = millivolts / 10;
char msg_out[20];
char msg_hr[20];
char msg_ic[20];

int spo2 = 0;

// Callback routine is executed when a pulse is detected
void onBeatDetected()
{
  Serial.println("Beat!");
  digitalWrite(ledB, !digitalRead(ledB));
  digitalWrite(buzzer, !digitalRead(buzzer));
}

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

void setup()
{
  for (int thisNote = 0; thisNote < notes * 2; thisNote = thisNote + 2)
  {

    // calculates the duration of each note
    divider = melody[thisNote + 1];
    if (divider > 0)
    {
      // regular note, just proceed
      noteDuration = (wholenote) / divider;
    }
    else if (divider < 0)
    {
      // dotted notes are represented with negative durations!!
      noteDuration = (wholenote) / abs(divider);
      noteDuration *= 1.5; // increases the duration in half for dotted notes
    }

    // we only play the note for 90% of the duration, leaving 10% as a pause
    tone(buzzer, melody[thisNote], noteDuration * 0.8);

    // Wait for the specief duration before playing the next note.
    delay(noteDuration);

    // stop the waveform generation before the next note.
    noTone(buzzer);
  }
  pinMode(D5, OUTPUT);
  pinMode(outputpin, INPUT);
  // Initialize sensor
  if (!pox.begin())
  {
    Serial.println("FAILED");
    for (;;)
    {
      buzzerError();
      delay(3000);
    }
  }
  else
  {
    Serial.println("SUCCESS");
    buzzerSuccess();
  }

  // Configure sensor to use 7.6mA for LED drive
  pox.setIRLedCurrent(MAX30100_LED_CURR_4_4MA);

  // Register a callback routine
  pox.setOnBeatDetectedCallback(onBeatDetected);
  // Set software serial baud to 115200;
  Serial.begin(9600);
  // connecting to a WiFi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to the WiFi network");
  buzzerSuccess();
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
      buzzerSuccess();
    }
    else
    {
      // print message
      Serial.print("failed with state ");
      Serial.print(client.state());
      buzzerError();
      delay(2000);
    }
  }
  // publish and subscribe
  client.subscribe(topic);
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

// 2 pips error song code
void buzzerError()
{
  digitalWrite(buzzer, HIGH);
  delay(300);
  digitalWrite(buzzer, LOW);
  delay(300);
  digitalWrite(buzzer, HIGH);
  delay(300);
  digitalWrite(buzzer, LOW);
}

// 3 pips success song code
void buzzerSuccess()
{
  digitalWrite(buzzer, HIGH);
  delay(300);
  digitalWrite(buzzer, LOW);
  delay(300);
  digitalWrite(buzzer, HIGH);
  delay(300);
  digitalWrite(buzzer, LOW);
  delay(300);
  digitalWrite(buzzer, HIGH);
  delay(300);
  digitalWrite(buzzer, LOW);
}

void loop()
{
  client.loop();
  // Read from the sensor
  pox.update();
  // Grab the updated heart rate and SpO2 levels
  if (millis() - tsLastReport > REPORTING_PERIOD_MS)
  {
    digitalWrite(buzzer, LOW);
    analogValue = analogRead(outputpin);
    millivolts = (analogValue / 1024.0) * 3300; // 3300 is the voltage provided by NodeMCU
    celsius = millivolts / 10;
    sprintf(msg_out, "%2.f", celsius);
    Serial.print("Temp : ");
    Serial.println(msg_out);
    // Publishe the data to the broker
    client.publish("moniteurCHU/temp", msg_out);
    spo2 = pox.getSpO2();
    sprintf(msg_hr, "%.2f", pox.getHeartRate());
    Serial.print("Heart Rate : ");
    Serial.println(pox.getHeartRate());
    client.publish("mntrCHU/plsRate", msg_hr);
    sprintf(msg_ic, "%d", pox.getSpO2());
    Serial.print("spo2 : ");
    Serial.println(pox.getSpO2());
    client.publish("moniteurCHU/spio2", msg_ic);
    tsLastReport = millis();
    delay(2000);
  }
}
