#include <Arduino.h>
#include "../include/config.h"
#include "WiFiManager.h"
#include "TemperatureSensor.h"
#include "TemperatureIndicator.h"
#include "TemperatureIndicatorManager.h"
#include "WebInterface.h"

// Skapa WiFiManager
WiFiManager wifiManager;

// Skapa temperatursensor (kan nu hantera flera sensorer)
TemperatureSensor tempSensor;

// Skapa temperaturindikator-manager
TemperatureIndicatorManager indicatorManager;

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
  
  // Lägg till indikatorer i managern
  indicatorManager.addIndicator(TEMP_LED_RED_PIN, TEMP_LED_GREEN_PIN, TEMP_LED_BLUE_PIN);
  indicatorManager.addIndicator(TEMP2_LED_RED_PIN, TEMP2_LED_GREEN_PIN, TEMP2_LED_BLUE_PIN);
  indicatorManager.addIndicator(TEMP3_LED_RED_PIN, TEMP3_LED_GREEN_PIN, TEMP3_LED_BLUE_PIN);
  
  // Initialisera temperatursensor
  if (tempSensor.begin()) {
    Serial.print("Temperature sensors initialized: ");
    Serial.print(tempSensor.getSensorCount());
    Serial.println(" sensors found");
  } else {
    Serial.println("Failed to initialize temperature sensors");
  }
  
  // Starta WiFiManager
  bool connected = wifiManager.begin();
  
  // Om ansluten till WiFi, starta webbservern
  if (connected) {
    // Starta webbgränssnittet med hela manager-objektet
    webInterface.begin(&wifiManager, &tempSensor, &indicatorManager);
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
    // Läs alla temperaturer
    tempSensor.readAllTemperatures();
    
    // Uppdatera alla indikatorer baserat på temperaturer
    int sensorCount = tempSensor.getSensorCount();
    for (int i = 0; i < sensorCount; i++) {
      if (tempSensor.isSensorFound(i)) {
        float temperature = tempSensor.getLastTemperature(i);
        
        // Uppdatera motsvarande indikator
        indicatorManager.updateIndicator(i, temperature);
      }
    }
    
    lastTempReadTime = millis();
  }
}
