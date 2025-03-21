# Destillationsmonitor - ESP32-firmware

Firmware för ESP32 som läser temperatursensorer och skickar data via WiFi till mobilappen.

## Funktioner

- Läsning av flera DS18B20 temperatursensorer
- Visuell indikation via RGB LEDs för varje sensor
- WiFi-anslutning för dataöverföring med statusindikation
- Inbyggd webbserver som exponerar ett REST API
- Konfigurerbara larmgränser för temperaturer
- Knappstyrning för grundläggande funktioner
- Strömsnål drift för långvarig användning

## Projektstruktur

```
esp32_code/
  ├── README.md                 (denna fil)
  ├── distillery_monitor/       (huvudprojektmapp för Arduino IDE/PlatformIO)
  │   ├── distillery_monitor.ino (huvudfil för Arduino IDE)
  │   ├── config.h              (konfigurationsfil för WiFi, sensorer, etc.)
  │   ├── sensors.cpp           (implementering av sensorfunktioner)
  │   ├── sensors.h             (deklarationer för sensorfunktioner)
  │   ├── wifi_manager.cpp      (hantering av WiFi-anslutning)
  │   ├── wifi_manager.h        (deklarationer för WiFi-funktioner)
  │   ├── api_server.cpp        (implementering av API-server)
  │   ├── api_server.h          (deklarationer för API-funktioner)
  │   ├── led_controller.cpp    (hantering av RGB LEDs)
  │   ├── led_controller.h      (deklarationer för LED-funktioner)
  │   ├── button_handler.cpp    (hantering av knappinput)
  │   └── button_handler.h      (deklarationer för knappfunktioner)
  └── libraries/                (externa bibliotek om de behövs lokalt)
```

## Hårdvarukrav

- ESP32 utvecklingskort (rekommendation: ESP32 DevKit V1 eller NodeMCU-ESP32)
- 3 st DS18B20 temperatursensorer (vattentäta versioner för destillation)
- 4.7kΩ resistor (för DS18B20 pull-up)
- 4 st RGB LEDs (common cathode rekommenderas)
- 12 st 470Ω resistorer (för RGB LEDs)
- 1 st tryckknapp
- 1 st 10kΩ resistor (för knapp pull-down)
- Kopplingsdäck och kablar för prototyping
- Micro USB-kabel för programmering och strömförsörjning

## Kopplingsschema

```
Temperatursensorer (DS18B20):
ESP32 GPIO4 ──────┬─────── DS18B20 #1 Data
                  ├─────── DS18B20 #2 Data
                  ├─────── DS18B20 #3 Data
                  │
                 4.7kΩ
                  │
3.3V ─────────────┴─────── DS18B20 #1, #2, #3 VDD
GND ────────────────────── DS18B20 #1, #2, #3 GND

RGB LED #1 (Sensor #1 - t.ex. Kolonntopp):
ESP32 GPIO25 ────┬── 470Ω ─── RGB LED #1 Röd
ESP32 GPIO26 ───┼── 470Ω ─── RGB LED #1 Grön
ESP32 GPIO27 ───┴── 470Ω ─── RGB LED #1 Blå
GND ──────────────────────── RGB LED #1 GND

RGB LED #2 (Sensor #2 - t.ex. Kolonnmitt):
ESP32 GPIO16 ────┬── 470Ω ─── RGB LED #2 Röd
ESP32 GPIO17 ───┼── 470Ω ─── RGB LED #2 Grön
ESP32 GPIO18 ───┴── 470Ω ─── RGB LED #2 Blå
GND ──────────────────────── RGB LED #2 GND

RGB LED #3 (Sensor #3 - t.ex. Kolonnbotten):
ESP32 GPIO19 ────┬── 470Ω ─── RGB LED #3 Röd
ESP32 GPIO21 ───┼── 470Ω ─── RGB LED #3 Grön
ESP32 GPIO22 ───┴── 470Ω ─── RGB LED #3 Blå
GND ──────────────────────── RGB LED #3 GND

RGB LED #4 (WiFi-status):
ESP32 GPIO12 ────┬── 470Ω ─── RGB LED #4 Röd
ESP32 GPIO13 ───┼── 470Ω ─── RGB LED #4 Grön
ESP32 GPIO14 ───┴── 470Ω ─── RGB LED #4 Blå
GND ──────────────────────── RGB LED #4 GND

Knapp:
ESP32 GPIO33 ─────────── Knapp
                │
               10kΩ
                │
GND ─────────────
```

## LED-färgkodning

### RGB LED #1-3 (Temperatursensorer):
- **Röd**: Temperatur över övre gräns (för hög)
- **Grön**: Temperatur inom optimalt intervall
- **Blå**: Temperatur under nedre gräns (för låg)
- **Lila** (röd+blå): Sensorn kunde inte läsas
- **Gul** (röd+grön): Varning (nära gräns)

### RGB LED #4 (WiFi):
- **Röd**: Ingen WiFi-anslutning
- **Grön**: Ansluten till WiFi
- **Blå**: Konfigurationsläge (t.ex. AP-läge)
- **Lila** (röd+blå): Försöker ansluta
- **Vit blink**: API-anrop tas emot

## Knappfunktioner

- **Kort tryck**: Tvinga fram WiFi-återanslutning
- **Långt tryck (3s)**: Starta AP-läge för WiFi-konfiguration
- **Mycket långt tryck (10s)**: Fabriksåterställning

## Nödvändiga bibliotek

- OneWire (för kommunikation med DS18B20)
- DallasTemperature (för att läsa DS18B20-sensorer)
- WiFi (inbyggt i ESP32 Arduino Core)
- WebServer (inbyggt i ESP32 Arduino Core)
- ArduinoJson (för att formatera API-svar)

## API-dokumentation

### Endpoints

- `GET /api/temperatures` - Hämtar aktuella temperaturer från alla sensorer
- `GET /api/temperature/:id` - Hämtar temperatur från en specifik sensor
- `GET /api/config` - Hämtar aktuell konfiguration
- `POST /api/config` - Uppdaterar konfiguration

### Exempel på API-svar

```json
{
  "sensors": [
    {
      "id": "28FF64448501234",
      "name": "Kolonntopp",
      "temperature": 78.5,
      "unit": "C"
    },
    {
      "id": "28FF6444851234",
      "name": "Kolonnmitt",
      "temperature": 85.1,
      "unit": "C"
    },
    {
      "id": "28FF6444852345",
      "name": "Kolonnbotten",
      "temperature": 92.3,
      "unit": "C"
    }
  ],
  "timestamp": 1621234567
}
```

## Installation och användning

1. Installera Arduino IDE (version 1.8.x eller senare)
2. Installera ESP32-stöd i Arduino IDE
3. Installera nödvändiga bibliotek via Arduino Library Manager
4. Öppna `distillery_monitor.ino` i Arduino IDE
5. Anpassa inställningar i `config.h`
6. Kompilera och ladda upp till ESP32

## Utveckling

### Förutsättningar

- Arduino IDE med ESP32-stöd eller PlatformIO
- Grundläggande kunskaper i C/C++
- Förståelse för Arduino-programmering

### Kompilering och uppladdning

1. Anslut ESP32 till datorn via USB
2. Välj rätt port i Arduino IDE
3. Välj "ESP32 Dev Module" som kort
4. Klicka på "Ladda upp"

## Felsökning

- **Sensorer läses inte korrekt**: Kontrollera kopplingar och resistor
- **WiFi ansluter inte**: Verifiera SSID och lösenord i config.h
- **API svarar inte**: Kontrollera IP-adress och brandväggsregler
- **LEDs lyser inte**: Kontrollera resistorer och anslutningar
- **Knappen fungerar inte**: Kontrollera pull-down resistor

## Licens

MIT