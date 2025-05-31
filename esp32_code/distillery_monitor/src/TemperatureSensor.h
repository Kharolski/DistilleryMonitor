#ifndef TEMPERATURE_SENSOR_H
#define TEMPERATURE_SENSOR_H

#include <Arduino.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include "../include/config.h"

// Maximalt antal sensorer som kan hanteras
#define MAX_SENSORS 3

class TemperatureSensor {
private:
  // Tre separata OneWire-bussar och DallasTemperature-objekt
  OneWire* oneWire1;
  OneWire* oneWire2;
  OneWire* oneWire3;
  
  DallasTemperature* sensors1;
  DallasTemperature* sensors2;
  DallasTemperature* sensors3;
  
  int sensorCount;
  bool sensorsFound[MAX_SENSORS];
  float lastTemperatures[MAX_SENSORS];
  DeviceAddress sensorAddresses[MAX_SENSORS];

public:
  TemperatureSensor() : sensorCount(0) {
    // Initiera pekare till nullptr
    oneWire1 = nullptr;
    oneWire2 = nullptr;
    oneWire3 = nullptr;
    sensors1 = nullptr;
    sensors2 = nullptr;
    sensors3 = nullptr;
    
    // Initiera arrays
    for (int i = 0; i < MAX_SENSORS; i++) {
      sensorsFound[i] = false;
      lastTemperatures[i] = 0.0;
      memset(sensorAddresses[i], 0, sizeof(DeviceAddress));
    }
  }

  ~TemperatureSensor() {
    // Rensa minne när objektet förstörs
    delete oneWire1;
    delete oneWire2;
    delete oneWire3;
    delete sensors1;
    delete sensors2;
    delete sensors3;
  }

  bool begin() {
    // Skapa OneWire-objekt för varje pin
    oneWire1 = new OneWire(TEMP_SENSOR_PIN_1);
    oneWire2 = new OneWire(TEMP_SENSOR_PIN_2);
    oneWire3 = new OneWire(TEMP_SENSOR_PIN_3);
    
    // Skapa DallasTemperature-objekt för varje OneWire-buss
    sensors1 = new DallasTemperature(oneWire1);
    sensors2 = new DallasTemperature(oneWire2);
    sensors3 = new DallasTemperature(oneWire3);
    
    // Aktivera intern pullup-resistor för alla pins
    pinMode(TEMP_SENSOR_PIN_1, INPUT_PULLUP);
    pinMode(TEMP_SENSOR_PIN_2, INPUT_PULLUP);
    pinMode(TEMP_SENSOR_PIN_3, INPUT_PULLUP);
    
    // Starta alla DallasTemperature-bibliotek
    sensors1->begin();
    sensors2->begin();
    sensors3->begin();
    
    sensorCount = 0;
    
    // Kontrollera sensor 1
    if (sensors1->getDeviceCount() > 0) {
      if (sensors1->getAddress(sensorAddresses[0], 0)) {
        Serial.print("Sensor 0 address: ");
        for (uint8_t j = 0; j < 8; j++) {
          if (sensorAddresses[0][j] < 16) Serial.print("0");
          Serial.print(sensorAddresses[0][j], HEX);
        }
        Serial.println();
        sensors1->setResolution(sensorAddresses[0], 10);
        sensorsFound[0] = true;
        sensorCount++;
      }
    }
    
    // Kontrollera sensor 2
    if (sensors2->getDeviceCount() > 0) {
      if (sensors2->getAddress(sensorAddresses[1], 0)) {
        Serial.print("Sensor 1 address: ");
        for (uint8_t j = 0; j < 8; j++) {
          if (sensorAddresses[1][j] < 16) Serial.print("0");
          Serial.print(sensorAddresses[1][j], HEX);
        }
        Serial.println();
        sensors2->setResolution(sensorAddresses[1], 10);
        sensorsFound[1] = true;
        sensorCount++;
      }
    }
    
    // Kontrollera sensor 3
    if (sensors3->getDeviceCount() > 0) {
      if (sensors3->getAddress(sensorAddresses[2], 0)) {
        Serial.print("Sensor 2 address: ");
        for (uint8_t j = 0; j < 8; j++) {
          if (sensorAddresses[2][j] < 16) Serial.print("0");
          Serial.print(sensorAddresses[2][j], HEX);
        }
        Serial.println();
        sensors3->setResolution(sensorAddresses[2], 10);
        sensorsFound[2] = true;
        sensorCount++;
      }
    }
    
    Serial.print("Found ");
    Serial.print(sensorCount);
    Serial.println(" temperature sensors");
    
    return sensorCount > 0;
  }

  // Läs temperatur från en specifik sensor
  float readTemperature(int sensorIndex = 0) {
    if (sensorIndex < 0 || sensorIndex >= MAX_SENSORS || !sensorsFound[sensorIndex]) {
      return lastTemperatures[sensorIndex];
    }
    
    DallasTemperature* currentSensor = nullptr;
    
    // Välj rätt sensor baserat på index
    switch (sensorIndex) {
      case 0:
        currentSensor = sensors1;
        break;
      case 1:
        currentSensor = sensors2;
        break;
      case 2:
        currentSensor = sensors3;
        break;
      default:
        return lastTemperatures[sensorIndex];
    }
    
    // Begär temperatur från sensorn
    currentSensor->requestTemperatures();
    
    // Läs temperatur med sensorns adress
    float tempC = currentSensor->getTempC(sensorAddresses[sensorIndex]);
    
    // Kontrollera om avläsningen lyckades
    if (tempC != DEVICE_DISCONNECTED_C) {
      lastTemperatures[sensorIndex] = tempC;
      Serial.print("Sensor ");
      Serial.print(sensorIndex);
      Serial.print(" temperature: ");
      Serial.print(tempC);
      Serial.println(" °C");
    } else {
      Serial.print("Error reading temperature from sensor ");
      Serial.println(sensorIndex);
    }
    
    return lastTemperatures[sensorIndex];
  }

  // Läs alla temperaturer på en gång
  void readAllTemperatures() {
    // Läs från varje sensor individuellt
    for (int i = 0; i < MAX_SENSORS; i++) {
      if (sensorsFound[i]) {
        readTemperature(i);
      }
    }
  }

  // Hämta senast lästa temperatur för en sensor
  float getLastTemperature(int sensorIndex = 0) {
    if (sensorIndex >= 0 && sensorIndex < MAX_SENSORS) {
      return lastTemperatures[sensorIndex];
    }
    return 0.0;
  }

  // Kontrollera om en specifik sensor hittades
  bool isSensorFound(int sensorIndex = 0) {
    if (sensorIndex >= 0 && sensorIndex < MAX_SENSORS) {
      return sensorsFound[sensorIndex];
    }
    return false;
  }

  // Hämta antalet sensorer som hittades
  int getSensorCount() {
    return sensorCount;
  }
};

#endif
