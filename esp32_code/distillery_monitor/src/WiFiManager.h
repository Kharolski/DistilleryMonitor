#ifndef WIFI_MANAGER_H
#define WIFI_MANAGER_H

#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <Preferences.h>
#include "../include/config.h"

class WiFiManager {
private:
  WebServer configServer;
  bool apMode;
  String ssid;
  String password;
  Preferences preferences;
  
  // Function to set RGB LED color
  void setLedColor(int red, int green, int blue) {
    digitalWrite(LED_RED_PIN, red);
    digitalWrite(LED_GREEN_PIN, green);
    digitalWrite(LED_BLUE_PIN, blue);
  }
  
  // Read WiFi settings from Preferences
  bool loadCredentials() {
    preferences.begin("wifi", false);
    ssid = preferences.getString("ssid", "");
    password = preferences.getString("password", "");
    preferences.end();
    
    return (ssid.length() > 0);
  }
  
  // Save WiFi settings to Preferences
  void saveCredentials() {
    preferences.begin("wifi", false);
    preferences.putString("ssid", ssid);
    preferences.putString("password", password);
    preferences.end();
  }
  
  // Configuration HTML
  String getConfigHTML() {
    String html = "<!DOCTYPE html><html>";
    html += "<head><meta name='viewport' content='width=device-width, initial-scale=1.0'>";
    html += "<title>WiFi Configuration</title>";
    html += "<link rel='icon' href='data:,'>";
    html += "<style>";
    html += "body { font-family: Arial, sans-serif; margin: 20px; }";
    html += ".container { max-width: 400px; margin: 0 auto; }";
    html += "input[type=text], input[type=password] { width: 100%; padding: 12px 20px; margin: 8px 0; display: inline-block; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }";
    html += "button { background-color: #4CAF50; color: white; padding: 14px 20px; margin: 8px 0; border: none; border-radius: 4px; cursor: pointer; width: 100%; }";
    html += "button:hover { background-color: #45a049; }";
    html += "</style></head>";
    html += "<body><div class='container'>";
    html += "<h1>WiFi Configuration</h1>";
    html += "<form action='/save' method='post'>";
    html += "SSID:<br><input type='text' name='ssid' value='" + ssid + "'><br>";
    html += "Password:<br><input type='password' name='password' value='" + password + "'><br>";
    html += "<button type='submit'>Save</button>";
    html += "</form></div></body></html>";
    return html;
  }
  
  // Handle root page
  void handleRoot() {
    configServer.send(200, "text/html", getConfigHTML());
  }
  
  // Handle saving settings
  void handleSave() {
    if (configServer.hasArg("ssid") && configServer.hasArg("password")) {
      ssid = configServer.arg("ssid");
      password = configServer.arg("password");
      
      // Save to Preferences
      saveCredentials();
      
      // Send confirmation page
      String html = "<!DOCTYPE html><html>";
      html += "<head><meta name='viewport' content='width=device-width, initial-scale=1.0'>";
      html += "<title>WiFi Configuration</title>";
      html += "<link rel='icon' href='data:,'>";
      html += "<style>body { font-family: Arial, sans-serif; margin: 20px; text-align: center; }</style>";
      html += "<meta http-equiv='refresh' content='5;url=/'>";
      html += "</head><body>";
      html += "<h1>Settings Saved</h1>";
      html += "<p>The device will restart and try to connect to the new network.</p>";
      html += "</body></html>";
      
      configServer.send(200, "text/html", html);
      
      // Wait a bit so the response can be sent
      delay(1000);
      
      // Restart ESP32
      ESP.restart();
    } else {
      configServer.send(400, "text/plain", "Invalid form");
    }
  }

public:
  WiFiManager() : configServer(80), apMode(false) {
    // Initialize with empty strings
    ssid = "";
    password = "";
  }
  
  // Start WiFi management
  bool begin() {
    // Configure LED pins
    pinMode(LED_RED_PIN, OUTPUT);
    pinMode(LED_GREEN_PIN, OUTPUT);
    pinMode(LED_BLUE_PIN, OUTPUT);
    
    // Set LED to blue (indicates startup)
    setLedColor(0, 0, 1);
    
    // Try to read saved settings
    if (loadCredentials() && ssid.length() > 0) {
      // Try to connect to saved network
      Serial.print("Connecting to saved network: ");
      Serial.println(ssid);
      
      WiFi.begin(ssid.c_str(), password.c_str());
      
      // Wait for connection
      unsigned long startTime = millis();
      bool ledState = false;
      
      while (WiFi.status() != WL_CONNECTED) {
        // Blink blue while waiting for connection
        ledState = !ledState;
        setLedColor(0, 0, ledState);
        
        delay(500);
        Serial.print(".");
        
        // If it takes too long, abort
        if (millis() - startTime > 20000) {
          Serial.println("WiFi connection timeout!");
          break;
        }
      }
      
      if (WiFi.status() == WL_CONNECTED) {
        // Connected - LED yellow (inactive but connected)
        setLedColor(1, 1, 0);
        
        Serial.println("");
        Serial.println("WiFi connected");
        Serial.print("IP address: ");
        Serial.println(WiFi.localIP());
        
        apMode = false;
        return true;
      }
    }
    
    // If we get here, we couldn't connect to the saved network
    // Start AP mode for configuration
    startConfigPortal();
    return false;
  }
  
  // Start the configuration portal
  void startConfigPortal() {
    Serial.println("Starting configuration portal");
    
    // Set LED to purple (configuration mode)
    setLedColor(1, 0, 1);
    
    // Start AP
    WiFi.softAP(AP_NAME, AP_PASSWORD);
    
    Serial.print("AP started with name: ");
    Serial.println(AP_NAME);
    Serial.print("IP address: ");
    Serial.println(WiFi.softAPIP());
    
    // Configure web server
    configServer.on("/", [this]() { this->handleRoot(); });
    configServer.on("/save", HTTP_POST, [this]() { this->handleSave(); });
    
    // Start web server
    configServer.begin();
    
    apMode = true;
  }
  
  // Check if we're in AP mode
  bool isAPMode() {
    return apMode;
  }
  
  // Handle web server in loop
  void process() {
    if (apMode) {
      configServer.handleClient();
    }
  }
  
  // Get IP address
  IPAddress getIP() {
    if (apMode) {
      return WiFi.softAPIP();
    } else {
      return WiFi.localIP();
    }
  }
  
  // Check WiFi status
  bool isConnected() {
    return (WiFi.status() == WL_CONNECTED);
  }
};

#endif
