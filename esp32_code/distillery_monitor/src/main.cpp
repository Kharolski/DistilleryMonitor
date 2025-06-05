#include <Arduino.h>
#include "../include/config.h"
#include "WiFiManager.h"
#include "TemperatureSensor.h"
#include "TemperatureIndicator.h"
#include "TemperatureIndicatorManager.h"
#include "WebInterface.h"
#include "DisplayManager.h"

// Skapa objekt
WiFiManager wifiManager;
TemperatureSensor tempSensor;
TemperatureIndicatorManager indicatorManager;
WebInterface webInterface;
DisplayManager displayManager;

// Display-hantering variabler
static unsigned long lastDisplayUpdate = 0;
static unsigned long ipShowStartTime = 0;
static bool showingIPAfterConnect = false;

// Global variabel för att tvinga AP-läge
static bool forceConfigMode = false;

// Knapp-hantering
void handleButtonPress() {
  if (digitalRead(BUTTON_PIN) == LOW) {
    delay(BUTTON_DEBOUNCE_MS);
    
    if (digitalRead(BUTTON_PIN) == LOW) {
      unsigned long pressStart = millis();
      
      // Vänta på släpp eller långt tryck
      while (digitalRead(BUTTON_PIN) == LOW) {
        if (millis() - pressStart > LONG_PRESS_MS) {
          // LÅNGT TRYCK = Config-läge (UTAN omstart!)
          Serial.println("Long press - Starting config mode");
          
          // Stäng av webserver först
          webInterface.stop();
          
          // Starta config portal direkt
          forceConfigMode = true;
          wifiManager.startConfigPortal();
          
          // Visa config IP på display
          displayManager.showIPAddress(wifiManager.getIP(), true);
          displayManager.setMode(IP_MODE);
          
          Serial.println("Config mode started - AP IP: " + wifiManager.getIP().toString());
          return;
        }
        delay(10);
      }
      
      // KORT TRYCK = Toggle display mode (bara om inte i config-läge)
      if (!forceConfigMode && !wifiManager.isAPMode()) {
        DisplayMode currentMode = displayManager.getCurrentMode();
        if (currentMode == IP_MODE) {
          displayManager.setMode(TEMP_MODE);
          Serial.println("Switched to temperature mode");
        } else if (currentMode == TEMP_MODE) {
          displayManager.setMode(IP_MODE);
          Serial.println("Switched to IP mode");
        }
      }
    }
  }
}

void setup() {
  // Starta seriell kommunikation
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n\nStarting Distillation Monitor");
  
  // Initiera OLED display
  if (displayManager.begin()) {
    displayManager.showStartupScreen();
    delay(2000);  // Visa startup i 2 sekunder
  } else {
    Serial.println("Display initialization failed!");
  }
  
  // Konfigurera knapp (WiFiManager hanterar sina egna LED-pins)
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  
  // Lägg till indikatorer
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
  
  // Starta WiFiManager (hanterar sina egna LED-färger)
  bool connected = wifiManager.begin();
  
  if (connected && !forceConfigMode) {
    // Normal anslutning - visa IP och starta webserver
    IPAddress ip = wifiManager.getIP();
    displayManager.showIPAddress(ip, false);
    displayManager.setMode(IP_MODE);
    
    webInterface.begin(&wifiManager, &tempSensor, &indicatorManager);
    Serial.println("Web interface started");
  } else {
    // AP-läge (antingen första gången eller tvingad av knapp)
    displayManager.showIPAddress(wifiManager.getIP(), true);
    displayManager.setMode(IP_MODE);
  }
}

void loop() {
  // Hantera knapp
  handleButtonPress();
  
  // Hantera WiFiManager
  wifiManager.process();
  
  // AP-läge (config), visa bara config info
  if (wifiManager.isAPMode() || forceConfigMode) {
    if (millis() - lastDisplayUpdate > 1000) {
      displayManager.showIPAddress(wifiManager.getIP(), true);
      lastDisplayUpdate = millis();
    }
    
    // Kontrollera om config är klar
    if (forceConfigMode && wifiManager.isConnected()) {
      // Config klar - starta webserver och återgå till normal drift
      forceConfigMode = false;
      webInterface.begin(&wifiManager, &tempSensor, &indicatorManager);
      displayManager.setMode(IP_MODE);
      Serial.println("Config completed - returning to normal mode");
    }
    
    return;  // Hoppa över resten av loop när i config-läge
  }
  
  // Hantera webbgränssnitt
  webInterface.handleClient();
  
  // Smart display-logik
  if (wifiManager.isConnected()) {
    DisplayMode currentMode = displayManager.getCurrentMode();
    
    if (currentMode == IP_MODE) {
      // Visa IP-läge
      if (millis() - lastDisplayUpdate > 1000) {
        displayManager.showIPAddress(wifiManager.getIP(), false);
        lastDisplayUpdate = millis();
      }
    } else if (currentMode == TEMP_MODE) {
      // Visa temperatur-läge
      if (millis() - lastDisplayUpdate > 2000) {  // Uppdatera var 2:a sekund
        displayManager.showTemperatureStatus(&tempSensor, &indicatorManager, true);
        lastDisplayUpdate = millis();
      }
    }
  } else {
    // Visa startup-skärm vid frånkoppling
    if (millis() - lastDisplayUpdate > 1000) {
      displayManager.showStartupScreen();
      lastDisplayUpdate = millis();
    }
  }
  
  // Läs temperaturer var 4:e sekund
  static unsigned long lastTempReadTime = 0;
  if (millis() - lastTempReadTime > 4000) {
    tempSensor.readAllTemperatures();
    
    int sensorCount = tempSensor.getSensorCount();
    for (int i = 0; i < sensorCount; i++) {
      if (tempSensor.isSensorFound(i)) {
        float temperature = tempSensor.getLastTemperature(i);
        indicatorManager.updateIndicator(i, temperature);
      }
    }
    
    lastTempReadTime = millis();
  }
}
