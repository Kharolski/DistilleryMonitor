#ifndef TEMPERATURE_SENSOR_H
#define TEMPERATURE_SENSOR_H

#include <Arduino.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include "../include/config.h"

class TemperatureSensor {
private:
  OneWire oneWire;
  DallasTemperature sensors;
  bool sensorFound;
  float lastTemperature;
  DeviceAddress sensorAddress;

public:
  TemperatureSensor() : oneWire(TEMP_SENSOR_PIN), sensors(&oneWire), sensorFound(false), lastTemperature(0.0) {
    // Initiera sensorAddress med nollor
    memset(sensorAddress, 0, sizeof(DeviceAddress));
  }

  bool begin() {
    // Aktivera intern pullup-resistor
    pinMode(TEMP_SENSOR_PIN, INPUT_PULLUP);
    
    // Start the DallasTemperature library
    sensors.begin();
    
    // Check if we can find any sensors
    int deviceCount = sensors.getDeviceCount();
    
    if (deviceCount > 0) {
      Serial.print("Found ");
      Serial.print(deviceCount);
      Serial.println(" temperature sensors");
      
      // Get the address of the first sensor
      if (sensors.getAddress(sensorAddress, 0)) {
        Serial.print("Sensor address: ");
        for (uint8_t i = 0; i < 8; i++) {
          if (sensorAddress[i] < 16) Serial.print("0");
          Serial.print(sensorAddress[i], HEX);
        }
        Serial.println();
        
        // Set resolution to 10 bit (0.25 deg C)
        sensors.setResolution(sensorAddress, 10);
        
        sensorFound = true;
        return true;
      }
    }
    
    Serial.println("No temperature sensors found!");
    sensorFound = false;
    return false;
  }

  float readTemperature() {
    if (!sensorFound) {
      return lastTemperature;
    }
    
    // Request temperature from all sensors
    sensors.requestTemperatures();
    
    // Read temperature using the sensor address
    float tempC = sensors.getTempC(sensorAddress);
    
    // Check if reading was successful
    if (tempC != DEVICE_DISCONNECTED_C) {
      lastTemperature = tempC;
      Serial.print("Temperature: ");
      Serial.print(tempC);
      Serial.println(" °C");
    } else {
      Serial.println("Error reading temperature!");
    }
    
    return lastTemperature;
  }

  bool isSensorFound() {
    return sensorFound;
  }
};

#endif
