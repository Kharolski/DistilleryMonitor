#ifndef TEMPERATURE_INDICATOR_H
#define TEMPERATURE_INDICATOR_H

#include <Arduino.h>

// Färgkonstanter för tydlighet
enum LEDColor {
  LED_BLUE,    // Uppvärmning
  LED_GREEN,   // Optimal temperatur
  LED_YELLOW,  // Varningstemperatur (orange/gul)
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
    blueMaxTemp(50.0),    // Standard: Blå upp till 50°C
    greenMaxTemp(70.0),   // Standard: Grön 50-70°C
    yellowMaxTemp(80.0)   // Standard: Gul 70-80°C, Röd över 80°C
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
    
    // Använd PWM-värden (0-255) för bättre färgkontroll
    int r = 0, g = 0, b = 0;
    
    switch (color) {
    case LED_BLUE:
      r = 0; g = 0; b = 255;        // Ren blå
      break;
    case LED_GREEN:
      r = 0; g = 255; b = 0;        // Ren grön
      break;
    case LED_YELLOW:
      r = 255; g = 40; b = 0;       // Orange/gul (din inställning)
      break;
    case LED_RED:
      r = 255; g = 0; b = 0;        // Ren röd
      break;
    }
    
    // Invertera för common anode
    if (isCommonAnode) {
      r = 255 - r;
      g = 255 - g;
      b = 255 - b;
    }
    
    // Använd analogWrite för PWM
    analogWrite(redPin, r);
    analogWrite(greenPin, g);
    analogWrite(bluePin, b);
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
