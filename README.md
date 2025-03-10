# DistilleryMonitor - Temperaturövervakning för destillation

Detta projekt består av två delar: en Python/Kivy-app för mobilgränssnitt och ESP32-firmware för sensorer.

## Projektstruktur

```
DistilleryMonitor/
  ├── README.md               (huvudöversikt)
  ├── app/                    (Python/Kivy-appen)
  │   └── README.md           (app-specifik dokumentation)
  └── esp32_code/             (C/C++ för ESP32)
      └── README.md           (ESP32-specifik dokumentation)
```

## Python/Kivy-app
Mobilapp för att visa temperaturdata i realtid med grafer och notifieringar.

## ESP32-kod
Firmware för ESP32 som läser temperatursensorer och skickar data via WiFi.
