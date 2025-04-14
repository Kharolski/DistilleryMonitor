#ifndef WEB_INTERFACE_H
#define WEB_INTERFACE_H

#include <Arduino.h>
#include <WebServer.h>
#include "WiFiManager.h"
#include "TemperatureSensor.h"
#include "TemperatureIndicator.h"

class WebInterface {
private:
  WebServer server;
  WiFiManager* wifiManager;
  TemperatureSensor* tempSensor;
  TemperatureIndicator* tempIndicator;

public:
  WebInterface(int port = 80) : server(port) {
    wifiManager = nullptr;
    tempSensor = nullptr;
    tempIndicator = nullptr;
  }

  void begin(WiFiManager* wm, TemperatureSensor* ts, TemperatureIndicator* ti) {
    wifiManager = wm;
    tempSensor = ts;
    tempIndicator = ti;
    
    // Konfigurera webbserver
    server.on("/", [this]() { this->handleRoot(); });
    server.on("/refresh", [this]() { this->handleRefresh(); });
    server.on("/config", [this]() { this->handleConfig(); });
    server.on("/reset", [this]() { this->handleReset(); });
    server.on("/set-temp-ranges", [this]() { this->handleSetTempRanges(); });
    server.on("/favicon.ico", [this]() { this->handleFavicon(); });
    server.onNotFound([this]() { this->handleNotFound(); });
    
    // Starta webbservern
    server.begin();
    Serial.println("Web server started");
  }

  void handleClient() {
    server.handleClient();
  }

private:
  // Generera HTML för webbsidan
  String getHTML() {
    // Läs aktuell temperatur
    float temperature = tempSensor->readTemperature();
    
    // Uppdatera LED baserat på temperatur
    tempIndicator->updateLED(temperature);
    
    String html = "<!DOCTYPE html><html>";
    html += "<head><meta name='viewport' content='width=device-width, initial-scale=1.0'>";
    html += "<title>Distillation Monitor</title>";
    html += "<link rel='icon' href='data:,'>";  // Prevent favicon request
    html += "<meta http-equiv='refresh' content='60'>";  // Auto refresh every 60 seconds
    html += "<style>";
    html += "body { font-family: Arial, sans-serif; margin: 20px; }";
    html += ".container { max-width: 800px; margin: 0 auto; }";
    html += ".status-box { padding: 15px; margin: 15px 0; border-radius: 5px; background-color: #e9ecef; }";
    html += ".temperature { font-size: 24px; margin: 20px 0; padding: 15px; background-color: #d1ecf1; border-radius: 5px; color: #0c5460; }";
    html += ".temp-settings { margin: 20px 0; padding: 15px; background-color: #fff3cd; border-radius: 5px; }";
    html += "button { background-color: #007bff; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer; margin-right: 10px; margin-bottom: 10px; }";
    html += "button:hover { background-color: #0056b3; }";
    html += "input[type='number'] { width: 80px; padding: 5px; margin: 0 10px; }";
    html += ".footer { margin-top: 30px; font-size: 12px; color: #666; }";
    html += "</style></head>";
    html += "<body>";
    html += "<div class='container'>";
    html += "<h1>Distillation Monitor</h1>";
    
    // Visa temperatur
    html += "<div class='temperature'>";
    if (tempSensor->isSensorFound()) {
      html += "Temperature: " + String(temperature) + " &deg;C";
      html += " (LED Status: " + tempIndicator->getCurrentColorName() + ")";
    } else {
      html += "Temperature sensor not found!";
    }
    html += "</div>";
    
    // Temperaturintervall-inställningar
    html += "<div class='temp-settings'>";
    html += "<h2>Temperature Range Settings</h2>";
    html += "<form action='/set-temp-ranges' method='get'>";
    html += "<div>";
    html += "<label>Blue (Heating) up to: </label>";
    html += "<input type='number' name='blue-max' value='" + String(tempIndicator->getBlueMaxTemp()) + "' step='0.5'> &deg;C";
    html += "</div><div style='margin-top: 10px;'>";
    html += "<label>Green (Optimal) up to: </label>";
    html += "<input type='number' name='green-max' value='" + String(tempIndicator->getGreenMaxTemp()) + "' step='0.5'> &deg;C";
    html += "</div><div style='margin-top: 10px;'>";
    html += "<label>Yellow (Warning) up to: </label>";
    html += "<input type='number' name='yellow-max' value='" + String(tempIndicator->getYellowMaxTemp()) + "' step='0.5'> &deg;C";
    html += "</div><div style='margin-top: 10px;'>";
    html += "<p>Red (Too Hot): Above " + String(tempIndicator->getYellowMaxTemp()) + " &deg;C</p>";
    html += "</div><div style='margin-top: 10px;'>";
    html += "<button type='submit'>Save Temperature Ranges</button>";
    html += "</div>";
    html += "</form>";
    html += "</div>";
    
    // Visa systeminformation
    html += "<div class='status-box'>";
    html += "<h2>System Information</h2>";
    html += "<p>WiFi Status: " + String(wifiManager->isConnected() ? "Connected" : "Disconnected") + "</p>";
    html += "<p>IP Address: " + wifiManager->getIP().toString() + "</p>";
    html += "</div>";
    
    // Knappar
    html += "<div>";
    html += "<button onclick='location.href=\"/refresh\"'>Refresh Data</button>";
    html += "<button onclick='location.href=\"/config\"'>WiFi Settings</button>";
    html += "<button onclick='location.href=\"/reset\"'>Reset Device</button>";
    html += "</div>";
    
    html += "</div>";
    html += "</body></html>";
    
    return html;
  }

  // Hantera rotsidan
  void handleRoot() {
    server.send(200, "text/html", getHTML());
  }

  // Hantera uppdatering
  void handleRefresh() {
    server.send(200, "text/html", getHTML());
  }

  // Hantera temperaturintervall-inställningar
  void handleSetTempRanges() {
    if (server.hasArg("blue-max") && server.hasArg("green-max") && server.hasArg("yellow-max")) {
      float blueMax = server.arg("blue-max").toFloat();
      float greenMax = server.arg("green-max").toFloat();
      float yellowMax = server.arg("yellow-max").toFloat();
      
      // Validera att värdena är i stigande ordning
      if (blueMax < greenMax && greenMax < yellowMax) {
        tempIndicator->setTemperatureRanges(blueMax, greenMax, yellowMax);
        Serial.println("Temperature ranges updated");
      } else {
        Serial.println("Invalid temperature ranges (must be in ascending order)");
      }
    }
    
    // Omdirigera tillbaka till huvudsidan
    server.sendHeader("Location", "/", true);
    server.send(302, "text/plain", "");
  }

  // Hantera omdirigering till konfigurationsportalen
  void handleConfig() {
    wifiManager->startConfigPortal();
    
    String html = "<!DOCTYPE html><html>";
    html += "<head><meta name='viewport' content='width=device-width, initial-scale=1.0'>";
    html += "<title>Redirecting...</title>";
    html += "<link rel='icon' href='data:,'>";
    html += "<style>body { font-family: Arial, sans-serif; margin: 20px; text-align: center; }</style>";
    html += "</head><body>";
    html += "<h1>Starting Configuration Mode</h1>";
    html += "<p>The device has started a WiFi network named: " + String(AP_NAME) + "</p>";
    html += "<p>Connect to this network and go to <a href='http://192.168.4.1'>http://192.168.4.1</a> to configure WiFi settings.</p>";
    html += "</body></html>";
    
    server.send(200, "text/html", html);
    
    // Vänta lite så att svaret kan skickas
    delay(1000);
    
    // Starta om ESP32
    ESP.restart();
  }

  // Hantera enhetsåterställning
  void handleReset() {
    String html = "<!DOCTYPE html><html>";
    html += "<head><meta name='viewport' content='width=device-width, initial-scale=1.0'>";
    html += "<title>Resetting Device</title>";
    html += "<link rel='icon' href='data:,'>";
    html += "<style>body { font-family: Arial, sans-serif; margin: 20px; text-align: center; }</style>";
    html += "<meta http-equiv='refresh' content='5;url=/'>";
    html += "</head><body>";
    html += "<h1>Resetting Device</h1>";
    html += "<p>The device will restart in a few seconds...</p>";
    html += "</body></html>";
    
    server.send(200, "text/html", html);
    
    // Vänta lite så att svaret kan skickas
    delay(1000);
    
    // Starta om ESP32
    ESP.restart();
  }

  // Hantera favicon-förfrågan
  void handleFavicon() {
    server.send(204, "image/x-icon", "");  // Tomt svar med 204 No Content
  }

  // Hantera okända sökvägar
  void handleNotFound() {
    server.send(404, "text/plain", "Page not found");
  }
};

#endif
