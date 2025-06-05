#ifndef CONFIG_H
#define CONFIG_H

// Pindefinitioner för RGB-LED (WiFi status)
#define LED_RED_PIN 25     // Röd kanal på RGB-LED
#define LED_GREEN_PIN 26   // Grön kanal på RGB-LED
#define LED_BLUE_PIN 27    // Blå kanal på RGB-LED
#define BUTTON_PIN 33      // Knapp för att starta om WiFi

// DS18B20 temperatursensorer (separata pins)
#define TEMP_SENSOR_PIN_1 4   // GPIO pin för första DS18B20 temperatursensorn
#define TEMP_SENSOR_PIN_2 5   // GPIO pin för andra DS18B20 temperatursensorn  
#define TEMP_SENSOR_PIN_3 15  // GPIO pin för tredje DS18B20 temperatursensorn

// Bakåtkompatibilitet (kan tas bort senare)
#define TEMP_SENSOR_PIN 4     // Gamla definitionen

// RGB LED #1 för temperatursensor (Kolv)
#define TEMP_LED_RED_PIN 12    // GPIO pin för röd LED (temperatur)
#define TEMP_LED_GREEN_PIN 13  // GPIO pin för grön LED (temperatur)
#define TEMP_LED_BLUE_PIN 14   // GPIO pin för blå LED (temperatur)

// RGB LED #2 för temperatursensor (Destillat)
#define TEMP2_LED_RED_PIN 16    // GPIO pin för röd LED (temperatur)
#define TEMP2_LED_GREEN_PIN 17  // GPIO pin för grön LED (temperatur)
#define TEMP2_LED_BLUE_PIN 18   // GPIO pin för blå LED (temperatur)

// RGB LED #3 för temperatursensor (Kylare) - FLYTTADE PINS!
#define TEMP3_LED_RED_PIN 19    // GPIO pin för röd LED (temperatur)
#define TEMP3_LED_GREEN_PIN 23  // GPIO pin för grön LED (temperatur) - ÄNDRAD!
#define TEMP3_LED_BLUE_PIN 32   // GPIO pin för blå LED (temperatur) - ÄNDRAD!

// OLED Display I2C
#define OLED_SDA_PIN 21        // I2C Data pin
#define OLED_SCL_PIN 22        // I2C Clock pin
#define OLED_WIDTH 128         // OLED display width
#define OLED_HEIGHT 64         // OLED display height
#define OLED_ADDRESS 0x3C      // I2C address för OLED

// AP-inställningar (när i konfigurationsläge)
#define AP_NAME "DestillationMonitor"
#define AP_PASSWORD "password123"  // Minst 8 tecken
#define LONG_PRESS_MS 3000  // 3 sekunder för långt tryck

// Timeouts och fördröjningar
#define CONFIG_PORTAL_TIMEOUT_MS 180000  // 3 minuter timeout för konfigurationsportalen
#define BUTTON_DEBOUNCE_MS 50            // 50ms debounce för knappen
#define LONG_PRESS_MS 3000               // 3 sekunder för långt tryck (starta AP-läge)

#endif
