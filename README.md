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
```

3. Spara filen

4. Lägg till ändringar i Git:
   ```bash
   git add README.md
   ```

5. Committa ändringarna:
   ```bash
   git commit -m "Uppdatera README med korrekt formaterad projektstruktur"
   ```

6. Ladda upp till GitHub:
   ```bash
   git push origin main
   ```

## Viktiga detaljer:

1. **Trippla backticks (```)** är nyckeln för att skapa kodblock i markdown.
2. Se till att du har en tom rad före och efter kodblocket.
3. Lägg till språket om du vill ha syntaxfärgning, men för mappstrukturer kan du lämna det tomt.
4. Var noga med att varje rad har rätt indrag med mellanslag.