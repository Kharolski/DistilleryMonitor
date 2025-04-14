#ifndef TEMPERATURE_INDICATOR_H
#define TEMPERATURE_INDICATOR_H

#include <Arduino.h>

// Färgkonstanter för tydlighet
enum LEDColor {
  LED_BLUE,    // Uppvärmning
  LED_GREEN,   // Optimal temperatur
  LED_YELLOW,  // Varningstemperatur
  LED_RED      // För hög temperatur
};

class TemperatureIndicator {
private:
  // Temperaturintervall
  float blueMaxTemp;    // Blå upp till detta värde
  float greenMaxTemp;   // Grön upp till detta värde
  float yellowMaxTemp;  // Gul upp till detta värde
                       // Röd över yellowMaxTemp
  
  // LED-pins
  int redPin;
  int greenPin;
  int bluePin;
  
  // Aktuell LED-färg
  LEDColor currentColor;
  
  // Är LED:n för common anode eller common cathode?
  bool isCommonAnode;

public:
  // Konstruktor
  TemperatureIndicator(int redPin, int greenPin, int bluePin, bool isCommonAnode = false) : 
    redPin(redPin), 
    greenPin(greenPin), 
    bluePin(bluePin),
    isCommonAnode(isCommonAnode),
    currentColor(LED_BLUE),
    blueMaxTemp(70.0),    // Standard: Blå upp till 70°C
    greenMaxTemp(78.0),   // Standard: Grön 70-78°C
    yellowMaxTemp(85.0)   // Standard: Gul 78-85°C, Röd över 85°C
  {
    // Konfigurera pins
    pinMode(redPin, OUTPUT);
    pinMode(greenPin, OUTPUT);
    pinMode(bluePin, OUTPUT);
    
    // Sätt initial färg till blå
    setColor(LED_BLUE);
  }
  
  // Ställ in temperaturintervall
  void setTemperatureRanges(float blueMax, float greenMax, float yellowMax) {
    blueMaxTemp = blueMax;
    greenMaxTemp = greenMax;
    yellowMaxTemp = yellowMax;
  }
  
  // Uppdatera LED baserat på temperatur
  void updateLED(float temperature) {
    if (temperature <= blueMaxTemp) {
      setColor(LED_BLUE);
    } else if (temperature <= greenMaxTemp) {
      setColor(LED_GREEN);
    } else if (temperature <= yellowMaxTemp) {
      setColor(LED_YELLOW);
    } else {
      setColor(LED_RED);
    }
  }
  
  // Ställ in LED-färg
  void setColor(LEDColor color) {
    currentColor = color;
    
    // Standardvärden för common cathode (0 = av, 1 = på)
    int r = 0, g = 0, b = 0;
    
    switch (color) {
      case LED_BLUE:
        r = 0; g = 0; b = 1;
        break;
      case LED_GREEN:
        r = 0; g = 1; b = 0;
        break;
      case LED_YELLOW:
        r = 1; g = 1; b = 0;
        break;
      case LED_RED:
        r = 1; g = 0; b = 0;
        break;
    }
    
    // Invertera värden för common anode (1 = av, 0 = på)
    if (isCommonAnode) {
      r = !r;
      g = !g;
      b = !b;
    }
    
    digitalWrite(redPin, r);
    digitalWrite(greenPin, g);
    digitalWrite(bluePin, b);
  }
  
  // Hämta aktuell LED-färg
  LEDColor getCurrentColor() {
    return currentColor;
  }
  
  // Hämta temperaturintervall
  float getBlueMaxTemp() { return blueMaxTemp; }
  float getGreenMaxTemp() { return greenMaxTemp; }
  float getYellowMaxTemp() { return yellowMaxTemp; }
  
  // Konvertera färg till sträng för visning
  String getColorName(LEDColor color) {
    switch (color) {
      case LED_BLUE: return "Blue";
      case LED_GREEN: return "Green";
      case LED_YELLOW: return "Yellow";
      case LED_RED: return "Red";
      default: return "Unknown";
    }
  }
  
  // Hämta aktuell färg som sträng
  String getCurrentColorName() {
    return getColorName(currentColor);
  }
};

#endif
