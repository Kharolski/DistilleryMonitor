#ifndef APIHANDLER_H
#define APIHANDLER_H

#include <Arduino.h>
#include <ArduinoJson.h>
#include "TemperatureSensor.h"
#include "TemperatureIndicatorManager.h"

class ApiHandler {
private:
    TemperatureSensor* sensorManager;
    TemperatureIndicatorManager* indicatorManager;

public:
    ApiHandler(TemperatureSensor* sensors, TemperatureIndicatorManager* indicators) 
        : sensorManager(sensors), indicatorManager(indicators) {}

    String getTemperaturesJson() {
        DynamicJsonDocument doc(1024);
        JsonArray sensors = doc.createNestedArray("sensors");
        
        int sensorCount = sensorManager->getSensorCount();
        for (int i = 0; i < sensorCount; i++) {
            if (sensorManager->isSensorFound(i)) {
                JsonObject sensor = sensors.createNestedObject();
                sensor["id"] = i;
                sensor["name"] = getSensorName(i);
                sensor["temperature"] = sensorManager->getLastTemperature(i);
                sensor["status"] = getTemperatureStatus(i);
                sensor["led_color"] = getLedColor(i);
            }
        }
        
        doc["timestamp"] = millis();
        doc["sensor_count"] = sensorCount;
        
        String output;
        serializeJson(doc, output);
        return output;
    }

    String getConfigJson() {
        DynamicJsonDocument doc(512);
        
        int sensorCount = sensorManager->getSensorCount();
        for (int i = 0; i < sensorCount; i++) {
            JsonObject sensorConfig = doc.createNestedObject("sensor" + String(i));
            
            // Hämta nuvarande gränser från indicatorManager
            sensorConfig["blue_limit"] = indicatorManager->getBlueLimit(i);
            sensorConfig["green_limit"] = indicatorManager->getGreenLimit(i);
            sensorConfig["yellow_limit"] = indicatorManager->getYellowLimit(i);
            sensorConfig["name"] = getSensorName(i);
        }
        
        String output;
        serializeJson(doc, output);
        return output;
    }

    bool updateConfig(String jsonString) {
        DynamicJsonDocument doc(512);
        DeserializationError error = deserializeJson(doc, jsonString);
        
        if (error) {
            Serial.println("Failed to parse config JSON");
            return false;
        }

        // Uppdatera konfiguration för varje sensor
        int sensorCount = sensorManager->getSensorCount();
        for (int i = 0; i < sensorCount; i++) {
            String sensorKey = "sensor" + String(i);
            if (doc.containsKey(sensorKey)) {
                JsonObject sensorConfig = doc[sensorKey];
                
                if (sensorConfig.containsKey("blue_limit")) {
                    indicatorManager->setBlueLimit(i, sensorConfig["blue_limit"]);
                }
                if (sensorConfig.containsKey("green_limit")) {
                    indicatorManager->setGreenLimit(i, sensorConfig["green_limit"]);
                }
                if (sensorConfig.containsKey("yellow_limit")) {
                    indicatorManager->setYellowLimit(i, sensorConfig["yellow_limit"]);
                }
            }
        }
        
        return true;
    }

private:
    String getSensorName(int index) {
        switch(index) {
            case 0: return "Kolv";
            case 1: return "Destillat";
            case 2: return "Kylare";
            default: return "Sensor " + String(index);
        }
    }

    String getTemperatureStatus(int index) {
        float temp = sensorManager->getLastTemperature(index);
        
        if (temp < indicatorManager->getBlueLimit(index)) return "cold";
        if (temp < indicatorManager->getGreenLimit(index)) return "optimal";
        if (temp < indicatorManager->getYellowLimit(index)) return "warning";
        return "critical";
    }

    String getLedColor(int index) {
        float temp = sensorManager->getLastTemperature(index);
        
        if (temp < indicatorManager->getBlueLimit(index)) return "blue";
        if (temp < indicatorManager->getGreenLimit(index)) return "green";
        if (temp < indicatorManager->getYellowLimit(index)) return "yellow";
        return "red";
    }
};

#endif
