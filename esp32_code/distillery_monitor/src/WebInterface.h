#ifndef WEB_INTERFACE_H
#define WEB_INTERFACE_H

#include <Arduino.h>
#include <WebServer.h>
#include "WiFiManager.h"
#include "TemperatureSensor.h"
#include "TemperatureIndicator.h"
#include "TemperatureIndicatorManager.h"

class WebInterface {
private:
  WebServer server;
  WiFiManager* wifiManager;
  TemperatureSensor* tempSensor;
  TemperatureIndicatorManager* indicatorManager;

public:
  WebInterface(int port = 80) : server(port) {
    wifiManager = nullptr;
    tempSensor = nullptr;
    indicatorManager = nullptr;
  }

  void begin(WiFiManager* wm, TemperatureSensor* ts, TemperatureIndicatorManager* im) {
    wifiManager = wm;
    tempSensor = ts;
    indicatorManager = im;
    
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
    // Uppdatera alla temperaturer
    tempSensor->readAllTemperatures();
    
    // Beskrivande namn för sensorerna
    String sensorNames[] = {"Kolv Temperatur", "Destillat Temperatur", "Kylare Temperatur"};
    
    String html = "<!DOCTYPE html><html>";
    html += "<head><meta charset='UTF-8'>";
    html += "<head><meta name='viewport' content='width=device-width, initial-scale=1.0'>";
    html += "<title>Distillation Monitor</title>";
    html += "<link rel='icon' href='data:,'>";  // Prevent favicon request
    html += "<meta http-equiv='refresh' content='60'>";  // Auto refresh every 60 seconds
    html += "<style>";
    html += "body { font-family: Arial, sans-serif; margin: 20px; background-color: #f8f9fa; }";
    html += ".container { max-width: 1400px; margin: 0 auto; }";  // Bredare container
    html += ".status-box { padding: 15px; margin: 15px 0; border-radius: 8px; background-color: #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }";
    html += ".temperature { font-size: 18px; margin: 10px 0; padding: 15px; background-color: #d1ecf1; border-radius: 8px; color: #0c5460; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }";
    html += ".temp-settings { margin: 15px 0; padding: 15px; background-color: #fff3cd; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }";
    
    // Responsiv sensor container
    html += ".sensor-container { display: flex; flex-wrap: wrap; gap: 20px; justify-content: space-between; margin-bottom: 30px; }";
    html += ".sensor-box { flex: 1; min-width: 340px; max-width: 450px; background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }";
    
    html += "button { background-color: #007bff; color: white; border: none; padding: 12px 20px; border-radius: 6px; cursor: pointer; margin-right: 10px; margin-bottom: 10px; font-size: 14px; transition: background-color 0.3s; }";
    html += "button:hover { background-color: #0056b3; }";
    html += "input[type='number'] { width: 80px; padding: 8px; margin: 0 10px; border: 1px solid #ddd; border-radius: 4px; }";
    html += "label { font-weight: bold; color: #495057; }";
    html += ".footer { margin-top: 30px; font-size: 12px; color: #666; }";
    html += "h1 { text-align: center; color: #343a40; margin-bottom: 30px; }";
    html += "h2 { color: #495057; }";
    html += "h3 { margin-top: 0; color: #495057; border-bottom: 2px solid #dee2e6; padding-bottom: 10px; }";
    html += ".error { color: #dc3545; font-weight: bold; }";
    html += ".form-group { margin: 15px 0; }";
    html += ".form-group label { display: inline-block; width: 210px; }";
    
    // Media queries för responsivitet
    html += "@media (max-width: 1200px) { .sensor-box { min-width: 300px; } }";
    html += "@media (max-width: 900px) { .sensor-box { flex: 1 1 45%; min-width: 280px; } }";  // 2 per rad på mellanstora skärmar
    html += "@media (max-width: 600px) { .sensor-box { flex: 1 1 100%; min-width: auto; } }";  // 1 per rad på mobil
    html += "@media (max-width: 600px) { .form-group label { width: 100%; display: block; margin-bottom: 5px; } }";
    
    html += "</style></head>";
    html += "<body>";
    html += "<div class='container'>";
    html += "<h1>🌡️ Distillation Monitor</h1>";
    
    // Visa temperaturer för alla sensorer
    html += "<div class='sensor-container'>";
    
    int sensorCount = tempSensor->getSensorCount();
    for (int i = 0; i < sensorCount; i++) {
      TemperatureIndicator* indicator = indicatorManager->getIndicator(i);
      
      html += "<div class='sensor-box'>";
      html += "<div class='temperature'>";
      
      // Förbättrad rubrik med beskrivande namn
      html += "<h3>Sensor " + String(i + 1);
      if (i < 3) {
        html += " (" + sensorNames[i] + ")";
      }
      html += "</h3>";
      
      // Kontrollera om indikatorn finns
      if (indicator == nullptr) {
        html += "<p class='error'>Indikator " + String(i + 1) + " är inte konfigurerad!</p>";
        html += "<p>Kontrollera att alla indikatorer är registrerade i main.cpp</p>";
        html += "</div></div>"; // End temperature and sensor-box
        continue;
      }
      
      if (tempSensor->isSensorFound(i)) {
        float temperature = tempSensor->getLastTemperature(i);
        
        // Uppdatera LED baserat på temperatur
        indicator->updateLED(temperature);
        
        html += "<strong>Temperature:</strong> " + String(temperature) + " °C";
        html += "<br><strong>LED Status:</strong> " + indicator->getCurrentColorName();
      } else {
        html += "<p class='error'>Temperature sensor not found!</p>";
      }
      html += "</div>";
      
      // Temperaturintervall-inställningar för denna sensor (endast om indikator finns)
      if (indicator != nullptr) {
        html += "<div class='temp-settings'>";
        html += "<h3>⚙️ Temperature Range Settings</h3>";
        html += "<form action='/set-temp-ranges' method='get'>";
        html += "<input type='hidden' name='sensor-id' value='" + String(i) + "'>";
        
        html += "<div class='form-group'>";
        html += "<label>🔵 Blue (Heating) up to:</label>";
        html += "<input type='number' name='blue-max' value='" + String(indicator->getBlueMaxTemp()) + "' step='0.5'> °C";
        html += "</div>";
        
        html += "<div class='form-group'>";
        html += "<label>🟢 Green (Optimal) up to:</label>";
        html += "<input type='number' name='green-max' value='" + String(indicator->getGreenMaxTemp()) + "' step='0.5'> °C";
        html += "</div>";
        
        html += "<div class='form-group'>";
        html += "<label>🟡 Yellow (Warning) up to:</label>";
        html += "<input type='number' name='yellow-max' value='" + String(indicator->getYellowMaxTemp()) + "' step='0.5'> °C";
        html += "</div>";
        
        html += "<div class='form-group'>";
        html += "<label>🔴 Red (Too Hot):</label>";
        html += "<span>Above " + String(indicator->getYellowMaxTemp()) + " °C</span>";
        html += "</div>";
        
        html += "<button type='submit'>💾 Save Temperature Ranges</button>";
        html += "</form>";
        html += "</div>";
      }
      html += "</div>"; // End sensor-box
    }
    
    html += "</div>"; // End sensor-container
    
    // Visa systeminformation
    html += "<div class='status-box'>";
    html += "<h2>📊 System Information</h2>";
    html += "<p><strong>WiFi Status:</strong> " + String(wifiManager->isConnected() ? "✅ Connected" : "❌ Disconnected") + "</p>";
    html += "<p><strong>IP Address:</strong> " + wifiManager->getIP().toString() + "</p>";
    html += "<p><strong>Number of Sensors:</strong> " + String(sensorCount) + "</p>";
    html += "<p><strong>Number of Indicators:</strong> " + String(indicatorManager->getIndicatorCount()) + "</p>";
    html += "</div>";
    
    // Knappar
    html += "<div style='text-align: center; margin-top: 30px;'>";
    html += "<button onclick='location.href=\"/refresh\"'>🔄 Refresh Data</button>";
    html += "<button onclick='location.href=\"/config\"'>📶 WiFi Settings</button>";
    html += "<button onclick='location.href=\"/reset\"'>🔄 Reset Device</button>";
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
    if (server.hasArg("sensor-id") &&
        server.hasArg("blue-max") &&
        server.hasArg("green-max") &&
        server.hasArg("yellow-max")) {
      
      int sensorId = server.arg("sensor-id").toInt();
      float blueMax = server.arg("blue-max").toFloat();
      float greenMax = server.arg("green-max").toFloat();
      float yellowMax = server.arg("yellow-max").toFloat();
      
      // Validera att värdena är i stigande ordning
      if (blueMax < greenMax && greenMax < yellowMax) {
        TemperatureIndicator* indicator = indicatorManager->getIndicator(sensorId);
        if (indicator != nullptr) {
          indicator->setTemperatureRanges(blueMax, greenMax, yellowMax);
          Serial.print("Temperature ranges updated for sensor ");
          Serial.println(sensorId);
        }
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
