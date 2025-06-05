#ifndef WIFI_MANAGER_H
#define WIFI_MANAGER_H

#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <Preferences.h>
#include "../include/config.h"
#include <ESPmDNS.h>

class WiFiManager {
private:
  WebServer configServer;
  bool apMode;
  String ssid;
  String password;
  Preferences preferences;
  
  // Skanna efter tillgängliga WiFi-nätverk
  String scanWiFiNetworks() {
    Serial.println("Scanning for WiFi networks...");
    int n = WiFi.scanNetworks();
    String options = "";
    
    if (n == 0) {
      options = "<option value=''>No networks found</option>";
    } else {
      options = "<option value=''>Select network...</option>";
      
      for (int i = 0; i < n; ++i) {
        String ssidName = WiFi.SSID(i);
        String security = (WiFi.encryptionType(i) == WIFI_AUTH_OPEN) ? " (Open)" : " (Secured)";
        int rssi = WiFi.RSSI(i);
        
        // Signalstyrka med enkla symboler
        String signal = "";
        if (rssi > -50) signal = "●●●●";      // Mycket stark
        else if (rssi > -60) signal = "●●●○";  // Stark  
        else if (rssi > -70) signal = "●●○○";  // Medium
        else signal = "●○○○";                  // Svag
        
        // HTML-escape för säkerhet
        ssidName.replace("&", "&amp;");
        ssidName.replace("<", "&lt;");
        ssidName.replace(">", "&gt;");
        ssidName.replace("\"", "&quot;");
        
        options += "<option value='" + ssidName + "'>";
        options += ssidName + " " + signal + security;
        options += "</option>";
      }
    }
    
    return options;
  }

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
    // Skanna WiFi-nätverk först
    String wifiOptions = scanWiFiNetworks();
    
    String html = "<!DOCTYPE html><html>";
    html += "<head>";
    html += "<meta charset='UTF-8'>";
    html += "<meta name='viewport' content='width=device-width, initial-scale=1.0'>";
    html += "<title>WiFi Configuration</title>";
    html += "<link rel='icon' href='data:,'>";
    html += "<style>";
    html += "body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }";
    html += ".container { max-width: 500px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }";
    html += "h1 { color: #333; text-align: center; }";
    html += "label { display: block; margin-top: 15px; font-weight: bold; color: #555; }";
    html += "select, input[type=text], input[type=password] { width: 100%; padding: 12px; margin: 8px 0; border: 2px solid #ddd; border-radius: 6px; box-sizing: border-box; font-size: 16px; }";
    html += "select:focus, input:focus { border-color: #4CAF50; outline: none; }";
    html += "button { background-color: #4CAF50; color: white; padding: 15px 20px; margin: 20px 0; border: none; border-radius: 6px; cursor: pointer; width: 100%; font-size: 16px; }";
    html += "button:hover { background-color: #45a049; }";
    html += ".refresh-btn { background-color: #2196F3; margin-bottom: 10px; }";
    html += ".refresh-btn:hover { background-color: #1976D2; }";
    html += ".manual-input { margin-top: 10px; }";
    html += ".info { background-color: #e7f3ff; padding: 10px; border-radius: 5px; margin: 10px 0; }";
    html += "</style>";
    
    // JavaScript samma som innan...
    html += "<script>";
    html += "function toggleManualInput() {";
    html += "  var select = document.getElementById('wifiSelect');";
    html += "  var manual = document.getElementById('manualSSID');";
    html += "  if (select.value === 'MANUAL') {";
    html += "    manual.style.display = 'block';";
    html += "    manual.focus();";
    html += "  } else {";
    html += "    manual.style.display = 'none';";
    html += "    document.getElementById('ssid').value = select.value;";
    html += "  }";
    html += "}";
    html += "</script>";
    
    html += "</head>";
    html += "<body><div class='container'>";
    html += "<h1>WiFi Configuration</h1>";
    
    html += "<div class='info'>";
    html += "<strong>Instructions:</strong><br>";
    html += "1. Select your WiFi network from the list<br>";
    html += "2. Enter password<br>";
    html += "3. Click 'Connect'<br>";
    html += "<em>After setup, access via: <strong>http://distillation.local/</strong></em>";
    html += "</div>";
    
    html += "<form action='/save' method='post'>";
    html += "<button type='button' class='refresh-btn' onclick='location.reload()'>Refresh Networks</button>";
    html += "<label for='wifiSelect'>Select WiFi Network:</label>";
    html += "<select id='wifiSelect' onchange='toggleManualInput()'>";
    html += wifiOptions;
    html += "<option value='MANUAL'>Enter manually...</option>";
    html += "</select>";
    
    html += "<div id='manualSSID' class='manual-input' style='display:none;'>";
    html += "<label for='manualInput'>Enter SSID manually:</label>";
    html += "<input type='text' id='manualInput' placeholder='Enter WiFi name'>";
    html += "</div>";
    
    html += "<input type='hidden' id='ssid' name='ssid' value='" + ssid + "'>";
    html += "<label for='password'>WiFi Password:</label>";
    html += "<input type='password' id='password' name='password' value='' placeholder='Enter password'>";
    html += "<button type='submit'>Connect to WiFi</button>";
    html += "</form></div>";
    
    // JavaScript för formulär...
    html += "<script>";
    html += "document.querySelector('form').onsubmit = function() {";
    html += "  var select = document.getElementById('wifiSelect');";
    html += "  var ssidField = document.getElementById('ssid');";
    html += "  if (select.value === 'MANUAL') {";
    html += "    ssidField.value = document.getElementById('manualInput').value;";
    html += "  } else {";
    html += "    ssidField.value = select.value;";
    html += "  }";
    html += "  return ssidField.value.length > 0;";
    html += "};";
    html += "</script>";
    
    html += "</body></html>";
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
      
      saveCredentials();
      
      String html = "<!DOCTYPE html><html>";
      html += "<head>";
      html += "<meta charset='UTF-8'>";
      html += "<meta name='viewport' content='width=device-width, initial-scale=1.0'>";
      html += "<title>WiFi Configuration</title>";
      html += "<style>";
      html += "body { font-family: Arial, sans-serif; margin: 20px; text-align: center; background-color: #f5f5f5; }";
      html += ".container { max-width: 450px; margin: 50px auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }";
      html += ".success { color: #4CAF50; font-size: 24px; margin-bottom: 20px; }";
      html += ".countdown { font-size: 18px; color: #2196F3; font-weight: bold; margin: 20px 0; }";
      html += ".link-box { background-color: #e7f3ff; padding: 20px; border-radius: 8px; margin: 20px 0; }";
      html += ".link { color: #1976D2; font-size: 18px; font-weight: bold; text-decoration: none; }";
      html += ".link:hover { text-decoration: underline; }";
      html += "</style>";
      html += "</head><body>";
      
      html += "<div class='container'>";
      html += "<div class='success'>✅ WiFi Settings Saved!</div>";
      html += "<p><strong>Network:</strong> " + ssid + "</p>";
      html += "<p>Device is restarting and connecting...</p>";
      html += "<div class='countdown' id='countdown'>Please wait 25 seconds...</div>";
      
      html += "<div class='link-box'>";
      html += "<p><strong>Easy Access Link:</strong></p>";
      html += "<a href='http://distillation.local/' class='link' id='accessLink'>http://distillation.local/</a>";
      html += "<p><small>Bookmark this link for future access!</small></p>";
      html += "</div>";
      
      html += "<div id='status'></div>";
      html += "</div>";
      
      // JavaScript med mDNS redirect
      html += "<script>";
      html += "var timeLeft = 25;";
      html += "var countdownEl = document.getElementById('countdown');";
      html += "var statusEl = document.getElementById('status');";
      html += "var linkEl = document.getElementById('accessLink');";
      html += "";
      html += "var timer = setInterval(function() {";
      html += "  if (timeLeft > 20) {";
      html += "    countdownEl.innerHTML = 'Device restarting... ' + timeLeft + 's';";
      html += "  } else if (timeLeft > 15) {";
      html += "    countdownEl.innerHTML = 'Connecting to WiFi... ' + timeLeft + 's';";
      html += "  } else if (timeLeft > 10) {";
      html += "    countdownEl.innerHTML = 'Starting web server... ' + timeLeft + 's';";
      html += "  } else if (timeLeft > 5) {";
      html += "    countdownEl.innerHTML = 'Almost ready... ' + timeLeft + 's';";
      html += "    linkEl.style.backgroundColor = '#4CAF50';";
      html += "    linkEl.style.color = 'white';";
      html += "    linkEl.style.padding = '10px';";
      html += "    linkEl.style.borderRadius = '5px';";
      html += "  } else if (timeLeft > 0) {";
      html += "    countdownEl.innerHTML = 'Redirecting in ' + timeLeft + 's...';";
      html += "  } else {";
      html += "    clearInterval(timer);";
      html += "    countdownEl.innerHTML = 'Redirecting now...';";
      html += "    statusEl.innerHTML = '<p style=\"color: #4CAF50; font-weight: bold;\">🚀 Redirecting to your device...</p>';";
      html += "    window.location.href = 'http://distillation.local/';";
      html += "  }";
      html += "  timeLeft--;";
      html += "}, 1000);";
      html += "</script>";
      
      html += "</body></html>";
      
      configServer.send(200, "text/html", html);
      delay(2000);
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
        // Connected - LED green (inactive but connected)
        setLedColor(0, 1, 0);
        
        Serial.println("");
        Serial.println("WiFi connected");
        Serial.print("IP address: ");
        Serial.println(WiFi.localIP());
        
        // Starta mDNS så man kan komma åt via http://distillation.local
        if (!MDNS.begin("distillation")) {
          Serial.println("Error setting up MDNS responder!");
        } else {
          Serial.println("mDNS responder started - access via http://distillation.local");
        }

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
