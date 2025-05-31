#ifndef TEMPERATURE_INDICATOR_MANAGER_H
#define TEMPERATURE_INDICATOR_MANAGER_H

#include "TemperatureIndicator.h"

// Maximalt antal indikatorer som kan hanteras
#define MAX_INDICATORS 3

class TemperatureIndicatorManager {
private:
  TemperatureIndicator* indicators[MAX_INDICATORS];
  int indicatorCount;

public:
  TemperatureIndicatorManager() : indicatorCount(0) {
    // Initiera array med nullptr
    for (int i = 0; i < MAX_INDICATORS; i++) {
      indicators[i] = nullptr;
    }
  }

  ~TemperatureIndicatorManager() {
    // Frigör minne för alla indikatorer
    for (int i = 0; i < indicatorCount; i++) {
      if (indicators[i] != nullptr) {
        delete indicators[i];
        indicators[i] = nullptr;
      }
    }
  }

  // Lägg till en ny indikator
  bool addIndicator(int redPin, int greenPin, int bluePin, bool isCommonAnode = false) {
    if (indicatorCount >= MAX_INDICATORS) {
      Serial.println("Maximum number of indicators reached");
      return false;
    }

    indicators[indicatorCount] = new TemperatureIndicator(redPin, greenPin, bluePin, isCommonAnode);
    indicatorCount++;
    
    Serial.print("Added indicator #");
    Serial.print(indicatorCount);
    Serial.println(" to manager");
    
    return true;
  }

  // Uppdatera en specifik indikator baserat på temperatur
  void updateIndicator(int index, float temperature) {
    if (index >= 0 && index < indicatorCount && indicators[index] != nullptr) {
      indicators[index]->updateLED(temperature);
    }
  }

  // Uppdatera alla indikatorer baserat på temperaturer
  void updateAllIndicators(float* temperatures) {
    for (int i = 0; i < indicatorCount; i++) {
      if (indicators[i] != nullptr) {
        indicators[i]->updateLED(temperatures[i]);
      }
    }
  }

  // Hämta en specifik indikator
  TemperatureIndicator* getIndicator(int index) {
    if (index >= 0 && index < indicatorCount) {
      return indicators[index];
    }
    return nullptr;
  }

  // Hämta antalet indikatorer
  int getIndicatorCount() {
    return indicatorCount;
  }

  // Ställ in temperaturintervall för en specifik indikator
  void setTemperatureRanges(int index, float blueMax, float greenMax, float yellowMax) {
    if (index >= 0 && index < indicatorCount && indicators[index] != nullptr) {
      indicators[index]->setTemperatureRanges(blueMax, greenMax, yellowMax);
    }
  }

  // Ställ in samma temperaturintervall för alla indikatorer
  void setAllTemperatureRanges(float blueMax, float greenMax, float yellowMax) {
    for (int i = 0; i < indicatorCount; i++) {
      if (indicators[i] != nullptr) {
        indicators[i]->setTemperatureRanges(blueMax, greenMax, yellowMax);
      }
    }
  }
};

#endif
