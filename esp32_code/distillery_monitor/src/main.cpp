#include <Arduino.h>
#include "../include/config.h"
#include "WiFiManager.h"
#include "TemperatureSensor.h"
#include "TemperatureIndicator.h"
#include "WebInterface.h"

// Skapa WiFiManager
WiFiManager wifiManager;

// Skapa temperatursensor
TemperatureSensor tempSensor;

// Skapa temperaturindikator för LED
TemperatureIndicator tempIndicator(TEMP_LED_RED_PIN, TEMP_LED_GREEN_PIN, TEMP_LED_BLUE_PIN);

// Skapa webbgränssnitt
WebInterface webInterface;

// Funktion för att ställa in WiFi-status LED-färg
void setWifiLedColor(int red, int green, int blue) {
  digitalWrite(LED_RED_PIN, red);
  digitalWrite(LED_GREEN_PIN, green);
  digitalWrite(LED_BLUE_PIN, blue);
}

void setup() {
  // Starta seriell kommunikation
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n\nStarting Distillation Monitor");
  
  // Konfigurera WiFi-status RGB LED-pins
  pinMode(LED_RED_PIN, OUTPUT);
  pinMode(LED_GREEN_PIN, OUTPUT);
  pinMode(LED_BLUE_PIN, OUTPUT);
  
  // Konfigurera knapp
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  
  // Initialisera temperatursensor
  if (tempSensor.begin()) {
    Serial.println("Temperature sensor initialized");
  } else {
    Serial.println("Failed to initialize temperature sensor");
  }
  
  // Starta WiFiManager
  bool connected = wifiManager.begin();
  
  // Om ansluten till WiFi, starta webbservern
  if (connected) {
    // Starta webbgränssnittet
    webInterface.begin(&wifiManager, &tempSensor, &tempIndicator);
    Serial.println("Web interface started");
    
    // Ställ in WiFi-status LED till grön (ansluten och redo)
    setWifiLedColor(0, 1, 0);
  }
}

void loop() {
  // Hantera WiFiManager
  wifiManager.process();
  
  // Om i AP-läge, hantera endast WiFiManager
  if (wifiManager.isAPMode()) {
    return;
  }
  
  // Hantera webbgränssnitt
  webInterface.handleClient();
  
  // Kontrollera WiFi-status
  if (!wifiManager.isConnected()) {
    // Om frånkopplad, blinka rött
    static unsigned long lastBlinkTime = 0;
    static bool ledState = false;
    
    if (millis() - lastBlinkTime > 500) {
      ledState = !ledState;
      setWifiLedColor(ledState, 0, 0);
      lastBlinkTime = millis();
    }
  }
  
  // Kontrollera knapp för långt tryck (för att gå in i konfigurationsläge)
  if (digitalRead(BUTTON_PIN) == LOW) {
    // Knapp tryckt - vänta på debounce
    delay(BUTTON_DEBOUNCE_MS);
    
    // Om fortfarande tryckt efter debounce
    if (digitalRead(BUTTON_PIN) == LOW) {
      // Kontrollera för långt tryck
      unsigned long pressStartTime = millis();
      
      while (digitalRead(BUTTON_PIN) == LOW) {
        delay(10);
        
        // Om knappen hålls tillräckligt länge, starta konfigurationsläge
        if (millis() - pressStartTime > LONG_PRESS_MS) {
          Serial.println("Long button press detected - starting config mode");
          setWifiLedColor(1, 0, 1);  // Lila för konfigurationsläge
          wifiManager.startConfigPortal();
          ESP.restart();  // Starta om för att aktivera AP-läge
          return;
        }
      }
    }
  }
  
  // Läs temperatur periodiskt (var 4:e sekund)
  static unsigned long lastTempReadTime = 0;
  if (millis() - lastTempReadTime > 4000) {
    float temperature = tempSensor.readTemperature();
    
    if (tempSensor.isSensorFound()) {
      Serial.print("Temperature: ");
      Serial.print(temperature);
      Serial.println(" °C");
      
      // Uppdatera LED baserat på temperatur
      tempIndicator.updateLED(temperature);
    } else {
      Serial.println("Temperature sensor not found");
    }
    
    lastTempReadTime = millis();
  }
}
