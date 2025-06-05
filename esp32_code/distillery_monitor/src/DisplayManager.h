#ifndef DISPLAY_MANAGER_H
#define DISPLAY_MANAGER_H

#include <U8g2lib.h>
#include <Wire.h>
#include "config.h"
#include "TemperatureSensor.h"
#include "TemperatureIndicatorManager.h"

enum DisplayMode {
    STARTUP_MODE,
    IP_MODE,
    TEMP_MODE,
    CONFIG_MODE
};

class DisplayManager {
private:
    U8G2_SH1106_128X64_NONAME_F_HW_I2C display;
    DisplayMode currentMode;
    unsigned long lastBlinkTime;
    bool blinkState;
    
public:
    DisplayManager() : display(U8G2_R0, U8X8_PIN_NONE, OLED_SCL_PIN, OLED_SDA_PIN) {
        currentMode = STARTUP_MODE;
        lastBlinkTime = 0;
        blinkState = false;
    }
    
    bool begin() {
        display.begin();
        display.clearBuffer();
        display.setFont(u8g2_font_6x10_tf);
        display.drawStr(0, 15, "Display OK");
        display.sendBuffer();
        return true;
    }
    
    void showStartupScreen() {
        currentMode = STARTUP_MODE;
        display.clearBuffer();
        display.setFont(u8g2_font_6x10_tf);
        display.drawStr(0, 15, "Distillation");
        display.drawStr(0, 30, "Monitor");
        display.drawStr(0, 45, "Starting...");
        display.sendBuffer();
    }
    
    // WiFi-status med bakgrundsfärg (hela raden)
    void drawWiFiStatusBar(bool connected) {
        if (connected) {
            // Grön bakgrund = fylld rektangel överst
            display.drawBox(0, 0, 128, 8);  // Fylld rektangel hela bredden
            
            // Vit text på grön bakgrund (inverterad)
            display.setDrawColor(0);  // Vit färg (inverterad)
            display.setFont(u8g2_font_4x6_tf);
            display.drawStr(2, 6, "WiFi: ANSLUTEN");
            display.setDrawColor(1);  // Tillbaka till normal färg
        } else {
            // Röd bakgrund = blinkande fylld rektangel
            if (millis() - lastBlinkTime > 500) {
                blinkState = !blinkState;
                lastBlinkTime = millis();
            }
            
            if (blinkState) {
                display.drawBox(0, 0, 128, 8);  // Fylld rektangel (röd känsla)
                
                // Vit text på röd bakgrund
                display.setDrawColor(0);  // Inverterad färg
                display.setFont(u8g2_font_4x6_tf);
                display.drawStr(2, 6, "WiFi: FRANKOPPLAD");
                display.setDrawColor(1);  // Tillbaka till normal
            } else {
                // Tom ram när den blinkar
                display.drawFrame(0, 0, 128, 8);
                display.setFont(u8g2_font_4x6_tf);
                display.drawStr(2, 6, "WiFi: FRANKOPPLAD");
            }
        }
    }
    
    // Färgade cirklar för temperaturstatus
    void drawTemperatureStatusCircle(int x, int y, String colorName) {
        if (colorName == "Blue" || colorName == "BLA") {
            // Blå = tom cirkel
            display.drawCircle(x, y, 4);
        } else if (colorName == "Green" || colorName == "GRON") {
            // Grön = fylld cirkel
            display.drawDisc(x, y, 4);
        } else if (colorName == "Yellow" || colorName == "GUL") {
            // Gul = cirkel med kryss
            display.drawCircle(x, y, 4);
            display.drawLine(x-2, y-2, x+2, y+2);
            display.drawLine(x-2, y+2, x+2, y-2);
        } else if (colorName == "Red" || colorName == "ROD") {
            // Röd = fylld cirkel med ram
            display.drawDisc(x, y, 4);
            display.drawCircle(x, y, 5);
        }
    }
    
    // Offline-indikator (blinkande)
    void drawOfflineIndicator(int x, int y) {
        if (millis() - lastBlinkTime > 500) {
            blinkState = !blinkState;
            lastBlinkTime = millis();
        }
        
        if (blinkState) {
            // Blinkande fylld cirkel med X
            display.drawDisc(x, y, 4);
            display.setDrawColor(0);  // Vit färg för X
            display.drawLine(x-2, y-2, x+2, y+2);
            display.drawLine(x-2, y+2, x+2, y-2);
            display.setDrawColor(1);  // Tillbaka till normal
        } else {
            // Tom cirkel när den blinkar
            display.drawCircle(x, y, 4);
        }
    }
    
    void showIPAddress(IPAddress ip, bool isConfigMode) {
        currentMode = IP_MODE;
        display.clearBuffer();
        
        // WiFi status-bar överst
        drawWiFiStatusBar(!isConfigMode);
        
        display.setFont(u8g2_font_6x10_tf);
        
        if (isConfigMode) {
            display.drawStr(0, 22, "KONFIGURATION:");
            display.drawStr(0, 34, "Anslut WiFi:");
            display.setFont(u8g2_font_8x13_tf);
            display.drawStr(0, 48, AP_NAME);
            display.setFont(u8g2_font_6x10_tf);
            display.drawStr(0, 62, "192.168.4.1");
        } else {
            display.drawStr(0, 22, "WEBGRANSSNITT:");
            display.setFont(u8g2_font_8x13_tf);
            String ipStr = ip.toString();
            
            if (ipStr.length() > 15) {
                display.setFont(u8g2_font_6x10_tf);
            }
            
            display.drawStr(0, 40, ipStr.c_str());
            display.setFont(u8g2_font_6x10_tf);
            display.drawStr(0, 57, "Tryck knapp->Temp");
        }
        
        display.sendBuffer();
    }
    
    void showTemperatureStatus(TemperatureSensor* tempSensor, TemperatureIndicatorManager* indicatorManager, bool wifiConnected) {
        currentMode = TEMP_MODE;
        display.clearBuffer();
        
        // WiFi status-bar överst
        drawWiFiStatusBar(wifiConnected);
        
        display.setFont(u8g2_font_6x10_tf);
        display.drawStr(0, 20, "DESTILLATION:");
        
        String sensorNames[] = {"KOLV", "DEST", "KYL"};
        
        int sensorCount = tempSensor->getSensorCount();
        for (int i = 0; i < sensorCount && i < 3; i++) {
            int yPos = 32 + (i * 12);  // Lite mer plats för cirklar
            
            // Sensornamn
            display.drawStr(0, yPos, sensorNames[i].c_str());
            
            if (tempSensor->isSensorFound(i)) {
                // Temperatur
                float temp = tempSensor->getLastTemperature(i);
                String tempStr = String(temp, 1) + "C";
                display.drawStr(35, yPos, tempStr.c_str());
                
                // Färgad cirkel istället för text
                TemperatureIndicator* indicator = indicatorManager->getIndicator(i);
                if (indicator != nullptr) {
                    String colorName = indicator->getCurrentColorName();
                    drawTemperatureStatusCircle(100, yPos-3, colorName);  // Cirkel till höger
                }
            } else {
                // OFFLINE med blinkande cirkel
                drawOfflineIndicator(50, yPos-3);
                display.drawStr(60, yPos, "OFFLINE");
            }
        }
        
        display.sendBuffer();
    }
    
    DisplayMode getCurrentMode() { return currentMode; }
    void setMode(DisplayMode mode) { currentMode = mode; }
};

#endif
