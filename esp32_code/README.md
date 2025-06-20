# Destillationsmonitor - ESP32-firmware

Firmware för ESP32 som läser temperatursensorer och tillhandahåller data via:
- **Responsiv webbserver** för direktåtkomst via webbläsare
- **REST API** för mobilapp-integration och systemintegration
- **JSON-baserad datautbyte** för modern applikationsutveckling

## Funktioner

### Webbgränssnitt
- Responsiv design för desktop, tablet och mobil
- Realtidsvisning av temperaturer och LED-status
- Konfigurerbar temperaturintervall direkt i webbläsaren
- Automatisk uppdatering var 60:e sekund

### Display-funktioner
- **OLED 128x64 display** för lokal statusvisning
- **Realtidstemperaturer** visas kontinuerligt
- **WiFi-status och IP-adress** visas på displayen
- **Automatisk uppdatering** var 2:a sekund
- **Kompakt layout** med all viktig information

### REST API
- **JSON-baserade endpoints** för systemintegration
- **CORS-stöd** för webbappar och mobilappar
- **Realtidsdata** från alla temperatursensorer
- **Konfigurationshantering** via API
- **Standardiserat format** för enkel integration

### Hårdvarufunktioner
- Läsning av flera DS18B20 temperatursensorer (separata pins)
- Visuell indikation via RGB LEDs för varje sensor
- WiFi-anslutning med automatisk konfiguration
- WiFi-status LED med färgkodning
- Knappstyrning för WiFi-konfiguration
- Automatisk WiFi-återanslutning

## API-dokumentation

### Endpoints

#### GET /api/temperatures
Hämtar aktuella temperaturer från alla sensorer.

**Exempel-svar:**
```json
{
  "sensors": [
    {
      "id": 0,
      "name": "Kolv",
      "temperature": 65.3,
      "status": "optimal",
      "led_color": "green"
    },
    {
      "id": 1,
      "name": "Destillat",
      "temperature": 78.1,
      "status": "warning",
      "led_color": "yellow"
    },
    {
      "id": 2,
      "name": "Kylare",
      "temperature": 25.7,
      "status": "cold",
      "led_color": "blue"
    }
  ],
  "timestamp": 1234567890,
  "sensor_count": 3
}
```

#### GET /api/config
Hämtar nuvarande temperaturkonfiguration.

**Exempel-svar:**
```json
{
  "sensor0": {
    "blue_limit": 50.0,
    "green_limit": 70.0,
    "yellow_limit": 80.0,
    "name": "Kolv"
  },
  "sensor1": {
    "blue_limit": 50.0,
    "green_limit": 70.0,
    "yellow_limit": 80.0,
    "name": "Destillat"
  },
  "sensor2": {
    "blue_limit": 50.0,
    "green_limit": 70.0,
    "yellow_limit": 80.0,
    "name": "Kylare"
  }
}
```

#### POST /api/config
Uppdaterar temperaturkonfiguration.

**Exempel-förfrågan:**
```json
{
  "sensor0": {
    "blue_limit": 45.0,
    "green_limit": 75.0,
    "yellow_limit": 85.0
  }
}
```

**Exempel-svar:**
```json
{
  "status": "success"
}
```

### API-användningsexempel

#### JavaScript/Fetch
```javascript
// Hämta temperaturer
fetch('http://192.168.1.100/api/temperatures')
  .then(response => response.json())
  .then(data => {
    console.log('Temperaturer:', data.sensors);
  });

// Uppdatera konfiguration
fetch('http://192.168.1.100/api/config', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    sensor0: {
      blue_limit: 45.0,
      green_limit: 75.0,
      yellow_limit: 85.0
    }
  })
});
```

#### Python
```python
import requests

# Hämta temperaturer
response = requests.get('http://192.168.1.100/api/temperatures')
data = response.json()
print(f"Kolv temperatur: {data['sensors'][0]['temperature']}°C")

# Uppdatera konfiguration
config = {
    "sensor0": {
        "blue_limit": 45.0,
        "green_limit": 75.0,
        "yellow_limit": 85.0
    }
}
requests.post('http://192.168.1.100/api/config', json=config)
```

#### cURL
```bash
# Hämta temperaturer
curl http://192.168.1.100/api/temperatures

# Uppdatera konfiguration
curl -X POST http://192.168.1.100/api/config \
  -H "Content-Type: application/json" \
  -d '{"sensor0":{"blue_limit":45.0,"green_limit":75.0,"yellow_limit":85.0}}'
```

## Projektstruktur

```
esp32_code/
├── README.md                    (denna fil)
├── src/                         (källkodsfiler)
│   ├── main.cpp                 (huvudfil med setup och loop)
│   ├── WiFiManager.h            (WiFi-hantering med automatisk konfiguration)
│   ├── TemperatureSensor.h      (DS18B20 sensorhantering)
│   ├── TemperatureIndicator.h   (RGB LED-kontroll för temperaturindikation)
│   ├── TemperatureIndicatorManager.h (hantering av flera LED-indikatorer)
│   ├── WebInterface.h           (webbserver och HTML-gränssnitt)
│   ├── ApiHandler.h             (REST API-hantering och JSON-serialisering)
│   └── DisplayManager.h         (OLED-display hantering och UI)
├── include/
│   └── config.h                 (pin-definitioner och konfiguration)
└── platformio.ini               (PlatformIO konfiguration)
```

## Hårdvarukrav

- ESP32 utvecklingskort (ESP32 DevKit V1 eller liknande)
- 3 st DS18B20 temperatursensorer (vattentäta versioner rekommenderas)
- 4 st RGB LEDs (common cathode) - 3 för temperaturer + 1 för WiFi-status
- 12 st 220-470Ω resistorer (för RGB LEDs)
- 1 st tryckknapp (för WiFi-konfiguration)
- **1 st OLED-display 128x64 (SSD1306, I2C)**
- **3 st 4.7kΩ pull-up resistorer (för I2C och OneWire)**
- Kopplingsdäck och kablar
- Micro USB-kabel för programmering och strömförsörjning

## Kopplingsschema

```
Temperatursensorer (DS18B20) - Separata pins:
ESP32 GPIO4 ───── DS18B20 #1 Data (Kolv)
ESP32 GPIO5 ───── DS18B20 #2 Data (Destillat)  
ESP32 GPIO15 ──── DS18B20 #3 Data (Kylare)
3.3V ──────────── DS18B20 #1, #2, #3 VDD
GND ───────────── DS18B20 #1, #2, #3 GND
4.7kΩ ─────────── 3.3V till varje DS18B20 Data pin (pull-up)

OLED Display (128x64 SSD1306):
ESP32 GPIO21 ──── OLED SDA (I2C Data)
ESP32 GPIO22 ──── OLED SCL (I2C Clock)
3.3V ──────────── OLED VCC
GND ───────────── OLED GND

WiFi Status RGB LED:
ESP32 GPIO25 ── 470Ω ── WiFi LED Röd
ESP32 GPIO26 ── 470Ω ── WiFi LED Grön  
ESP32 GPIO27 ── 470Ω ── WiFi LED Blå
GND ──────────────────── WiFi LED GND

RGB LED #1 (Kolv Temperatur):
ESP32 GPIO12 ── 470Ω ── RGB LED #1 Röd
ESP32 GPIO13 ── 470Ω ── RGB LED #1 Grön  
ESP32 GPIO14 ── 470Ω ── RGB LED #1 Blå
GND ──────────────────── RGB LED #1 GND

RGB LED #2 (Destillat Temperatur):
ESP32 GPIO16 ── 470Ω ── RGB LED #2 Röd
ESP32 GPIO17 ── 470Ω ── RGB LED #2 Grön
ESP32 GPIO18 ── 470Ω ── RGB LED #2 Blå
GND ──────────────────── RGB LED #2 GND

RGB LED #3 (Kylare Temperatur):
ESP32 GPIO19 ── 470Ω ── RGB LED #3 Röd
ESP32 GPIO21 ── 470Ω ── RGB LED #3 Grön
ESP32 GPIO22 ── 470Ω ── RGB LED #3 Blå
GND ──────────────────── RGB LED #3 GND

Knapp (för WiFi-konfiguration):
ESP32 GPIO33 ── Knapp ── GND
```

## LED-färgkodning

### WiFi Status LED:
- **🔴 Röd (blinkande)**: Ingen WiFi-anslutning
- **🟢 Grön**: Ansluten till WiFi och redo
- **🟣 Lila**: Konfigurationsläge (AP-läge)

### RGB LEDs (Temperatursensorer):
- **🔵 Blå**: Uppvärmning (temperatur under blå gräns)
- **🟢 Grön**: Optimal temperatur (mellan blå och grön gräns)
- **🟡 Gul/Orange**: Varning (mellan grön och gul gräns)
- **🔴 Röd**: För hög temperatur (över gul gräns)

### Standard temperaturintervall:
- **Blå**: 0-50°C
- **Grön**: 50-70°C  
- **Gul**: 70-80°C
- **Röd**: >80°C

## Knappfunktioner

- **Långt tryck (3s)**: Starta konfigurationsläge för WiFi-inställningar

## Nödvändiga bibliotek

```ini
lib_deps = 
    paulstoffregen/OneWire@^2.3.7
    milesburton/DallasTemperature@^3.11.0
    tzapu/WiFiManager@^2.0.16-rc.2
    bblanchon/ArduinoJson@^6.21.3
    # mDNS ingår i ESP32 Arduino Core
```

## Installation och användning

### PlatformIO (rekommenderat):
1. Installera PlatformIO IDE eller VS Code med PlatformIO-tillägget
2. Öppna projektet i PlatformIO
3. Anslut ESP32 via USB
4. Kör `pio run -t upload` för att kompilera och ladda upp

### Arduino IDE:
1. Installera Arduino IDE (1.8.x eller senare)
2. Installera ESP32-stöd via Board Manager
3. Installera nödvändiga bibliotek via Library Manager
4. Kopiera alla .h-filer till Arduino-projektmappen
5. Kompilera och ladda upp main.cpp (döp om till .ino)

## Första användning

1. **Ladda upp firmware** till ESP32
2. **Anslut hårdvara** enligt kopplingsschema
3. **WiFi-konfiguration**:
   - ESP32 skapar ett WiFi-nätverk: "DestillationMonitor"
   - Anslut till detta nätverk med din telefon/dator
   - Öppna webbläsare och gå till 192.168.4.1
   - Välj ditt WiFi-nätverk och ange lösenord
4. **Hitta IP-adress**:
   - Kontrollera din routers DHCP-lista
   - Eller använd nätverksskanner
   - IP-adressen visas också i Serial Monitor
5. **Testa systemet**:
   - **Webbgränssnitt**: `http://[IP-ADRESS]/`
   - **API**: `http://[IP-ADRESS]/api/temperatures`

## Användningsområden

### Direktanvändning
- Öppna webbläsaren och gå till ESP32:s IP-adress
- Övervaka temperaturer i realtid
- Konfigurera temperaturintervall

### Systemintegration
- Bygg mobilappar med React Native, Flutter eller native utveckling
- Integrera med hemautomationssystem (Home Assistant, OpenHAB)
- Logga data till databaser (InfluxDB, MySQL, PostgreSQL)
- Skapa dashboards med Grafana eller liknande
- Automatisera processer baserat på temperaturdata

### Utvecklingsexempel
- **Mobilapp**: Använd API:et för att visa temperaturer i realtid
- **Datalogger**: Samla temperaturdata över tid för analys
- **Notifikationssystem**: Skicka varningar när temperaturer når kritiska nivåer
- **Automatisk styrning**: Styr pumpar, ventiler eller värmare baserat på temperaturdata

## Felsökning

### Vanliga problem:
- **Sensorer hittas inte**: Kontrollera kopplingar och pull-up resistorer
- **WiFi ansluter inte**: Använd konfigurationsknappen för att återställa WiFi-inställningar
- **API svarar inte**: Kontrollera att ESP32 är ansluten till samma nätverk
- **CORS-fel**: API:et har CORS-stöd aktiverat för alla origins

### Debug:
- Använd Serial Monitor (115200 baud) för debug-information
- Kontrollera IP-adress i Serial Monitor efter WiFi-anslutning

## Licens

MIT License

## Bidrag

Bidrag välkomnas! Skapa en pull request eller öppna en issue för buggar och funktionsförfrågningar.

## Changelog

### v2.1.0 (Senaste)
**WiFi Configuration Portal:**
- ✅ **Automatisk nätverksskanning** med signalstyrka-indikatorer (●●●○)
- ✅ **mDNS-stöd** för åtkomst via `http://distillation.local/`
- ✅ **Smart LED-feedback** under WiFi-konfiguration
- ✅ **UTF-8-stöd** för internationella WiFi-namn
- ✅ **Automatisk omdirigering** efter lyckad konfiguration
- ✅ **Professionell användarupplevelse** med countdown och statusmeddelanden

**Display-funktionalitet:**
- ✅ **OLED-display 128x64** (SSD1306) för lokal statusvisning
- ✅ **Realtidsvisning** av alla temperaturer och WiFi-status
- ✅ **Kompakt UI-design** med all viktig information synlig
- ✅ **Automatisk uppdatering** var 2:a sekund

### v2.0.0
- ✅ Lagt till REST API med JSON-stöd
- ✅ CORS-stöd för webbappar och mobilappar
- ✅ Strukturerad API-dokumentation
- ✅ Exempel för olika programmeringsspråk
- ✅ Förbättrad systemarkitektur med ApiHandler

### v1.0.0
- ✅ Grundläggande webbgränssnitt
- ✅ Temperatursensorstöd
- ✅ RGB LED-indikering
- ✅ WiFi-hantering
```
