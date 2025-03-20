#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>
#include "DHT.h"

// Wi-Fi credentials
const char* WIFI_SSID = "Galaxy A21D247";  //"Rakuten-9AD0";
const char* WIFI_PASSWORD = "roxl1010";    //"8TQ3MV23Y4";

// Firebase details
const char* FIREBASE_HOST = "project-dsa-2fc5f-default-rtdb.firebaseio.com";
const char* FIREBASE_API_KEY = "AIzaSyCkWVQhbNmKdh8dMG5hnAV0NjcXkyXiTNI";

WiFiClientSecure client;

// Sensor pins
#define DHTPIN 5  // D1
#define DHTTYPE DHT11
#define SOIL_MOISTURE_PIN A0 //D6
#define LDR_PIN 12 //D6
#define WATER_PUMP_PIN  2 // D4   //--4 //D2

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();
  pinMode(WATER_PUMP_PIN, OUTPUT);
  digitalWrite(WATER_PUMP_PIN, LOW);

  client.setInsecure(); // Ignore SSL certificate validation
  connectToWiFi();
}

void loop() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  int soilMoisture = analogRead(SOIL_MOISTURE_PIN);
  bool lightIntensity = digitalRead(LDR_PIN);

  Serial.print("Temp: "); Serial.print(temperature);
  Serial.print("C, Humidity: "); Serial.print(humidity);
  
  String state ="proper darkness";
  if(lightIntensity==0){
     Serial.print("%, intensity: "); Serial.print("High intensity");
     state = "proper brightness";
  }
  else{
     Serial.print("%, intensity: "); Serial.print("Low intensitye");
     state ="proper darkness";
  }
  
  Serial.print(", Soil moisture: "); Serial.print(soilMoisture);
  Serial.print(", Light: "); Serial.println(state);
  String pump;

  if (soilMoisture >= 700 ) { // Adjust threshold as needed
    digitalWrite(WATER_PUMP_PIN, HIGH);
    Serial.println("Water Pump ON");
    pump = "Water Pump ON";
  } else {
    digitalWrite(WATER_PUMP_PIN, LOW);
    Serial.println("Water Pump OFF");
    pump = "Water Pump OFF";
  }

  //controlWaterPump(soilMoisture,pump);
  updateFirebase(temperature, humidity, soilMoisture, state,pump);
  

  delay(1000);
}

void connectToWiFi() {
  Serial.print("Connecting to Wi-Fi");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnected to Wi-Fi");
}

void updateFirebase(float temperature, float humidity, int soilMoisture, String state,String Pump) {
  String path = "/sensorData.json?auth=" + String(FIREBASE_API_KEY);
  if (client.connect(FIREBASE_HOST, 443)) {
    StaticJsonDocument<200> doc;
    doc["temperature"] = temperature;
    doc["humidity"] = humidity;
    doc["soilMoisture"] = soilMoisture;
    doc["lightIntensity"] = state;
    doc["Pump"] = Pump;

    String json;
    serializeJson(doc, json);
    
    client.println("PUT " + path + " HTTP/1.1");
    client.println("Host: " + String(FIREBASE_HOST));
    client.println("Content-Type: application/json");
    client.println("Content-Length: " + String(json.length()));
    client.println();
    client.println(json);
    client.stop();
  }
}

void controlWaterPump(int soilMoisture,String pump) {
  if (soilMoisture >= 700 ) { // Adjust threshold as needed
    digitalWrite(WATER_PUMP_PIN, HIGH);
    Serial.println("Water Pump ON");
    pump = "Water Pump ON";
  } else {
    digitalWrite(WATER_PUMP_PIN, LOW);
    Serial.println("Water Pump OFF");
    pump = "Water Pump OFF";
  }
}
