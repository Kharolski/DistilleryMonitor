#ifndef CONFIG_H
#define CONFIG_H

// Pindefinitioner för RGB-LED
#define LED_RED_PIN 25     // Röd kanal på RGB-LED
#define LED_GREEN_PIN 26   // Grön kanal på RGB-LED
#define LED_BLUE_PIN 27    // Blå kanal på RGB-LED

#define BUTTON_PIN 33      // Knapp för att starta om WiFi

// #1 DS18B20 temperatursensor med rgb led
#define TEMP_SENSOR_PIN 4  // GPIO pin för DS18B20 temperatursensor
#define TEMP_LED_RED_PIN 12    // GPIO pin för röd LED (temperatur)
#define TEMP_LED_GREEN_PIN 13  // GPIO pin för grön LED (temperatur)
#define TEMP_LED_BLUE_PIN 14   // GPIO pin för blå LED (temperatur)

// AP-inställningar (när i konfigurationsläge)
#define AP_NAME "DestillationMonitor"
#define AP_PASSWORD "password123"  // Minst 8 tecken
#define LONG_PRESS_MS 3000  // 3 sekunder för långt tryck

// Timeouts och fördröjningar
#define CONFIG_PORTAL_TIMEOUT_MS 180000  // 3 minuter timeout för konfigurationsportalen
#define BUTTON_DEBOUNCE_MS 50            // 50ms debounce för knappen
#define LONG_PRESS_MS 3000               // 3 sekunder för långt tryck (starta AP-läge)

#endif
