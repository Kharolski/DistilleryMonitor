# Destillationsmonitor - Mobilapp

Mobilapp byggd med Kivy för att övervaka temperaturer i destillationsprocessen.

## Funktioner

- Realtidsvisning av temperaturer
- Grafisk representation av temperaturhistorik
- Notifieringar när temperaturer går utanför optimala intervall
- Persistent lagring av mätdata i lokal databas

## Projektstruktur

```
app/
  ├── main.py                     (huvudapplikationen, startpunkt)
  ├── README.md                   (projektdokumentation)
  ├── requirements.txt            (beroenden för appen)
  ├── assets/                     (mapp för bilder/ikoner/ljud)
  │   ├── icons/                  (ikoner för UI-element)
  │   └── sounds/                 (ljudfiler för notifikationer)
  │       ├── alarm.wav           (ljud för kritiska notifikationer)
  │       ├── notification.wav    (ljud för standardnotifikationer)
  │       ├── success.wav         (ljud för framgångsnotifikationer)
  │       └── warning.wav         (ljud för varningsnotifikationer)
  ├── screens/                    (separata skärmar i appen)
  │   ├── __init__.py             (gör mappen till ett Python-paket)
  │   ├── home_screen.py          (huvudskärm med temperaturkort)
  │   ├── detail_screen.py        (detaljvy med grafer)
  │   ├── about_screen.py         (information om appen)
  │   └── settings_screen.py      (inställningar, planerad)
  ├── components/                 (återanvändbara UI-komponenter)
  │   ├── __init__.py             (gör mappen till ett Python-paket)
  │   ├── temperature_card.py     (runda temperaturkort)
  │   ├── dropdown_menu.py        (dropdown-meny för navigering)
  │   ├── notification_toast.py   (visuell komponent för notifikationer)
  │   └── temperature_graph.py    (grafkomponent för temperaturhistorik)
  ├── notifications/              (notifikationshantering)
  │   ├── __init__.py             (gör mappen till ett Python-paket)
  │   ├── notification_manager.py (hantering av notifikationsvisning)
  │   └── notification_service.py (logik för notifikationsskapande)
  ├── services/                   (bakgrundstjänster)
  │   ├── __init__.py             (gör mappen till ett Python-paket)
  │   ├── background_monitor.py   (bakgrundsövervakning av sensorer)
  │   ├── platform_notifier.py    (plattformsspecifika notifikationer)
  │   └── sound_manager.py        (hantering av ljudnotifikationer)
  ├── data/                       (datahantering)
  │   ├── __init__.py             (gör mappen till ett Python-paket)
  │   ├── data_manager.py         (central datahanterings-klass)
  │   ├── data_provider.py        (basklass för datakällor)
  │   ├── mock_data_provider.py   (simulerad sensordata för testning)
  │   └── temperature_history.py  (hantering av temperaturhistorik)
  ├── database/                   (databashantering)
  │   ├── __init__.py             (gör mappen till ett Python-paket)
  │   ├── db_manager.py           (hanterar databasanslutningar)
  │   └── schema.py               (definierar databastabeller)
  └── models/                     (datamodeller)
      ├── __init__.py             (gör mappen till ett Python-paket)
      └── sensor_config.py        (konfiguration för sensorer)
```

## Filbeskrivningar:

Huvudfiler:

- `main.py` - Applikationens startpunkt som initierar och kör Kivy-appen
- `README.md` - Dokumentation och instruktioner för projektet
- `requirements.txt` - Listar alla Python-paket som krävs för att köra appen

Mappar och filer:

1. assets/
   - `icons/` - Innehåller ikoner för UI-element
   - `sounds/` - Ljudfiler för olika notifikationstyper (alarm, notifikation, framgång, varning)

2. screens/
   - `__init__.py` - Gör mappen till ett Python-paket
   - `home_screen.py` - Huvudskärmen som visar alla sensorers temperatur i kortform
   - `detail_screen.py` - Detaljvy för en enskild sensor med utökad information och grafer
   - `about_screen.py` - Informationssida om appen och dess syfte
   - `settings_screen.py` - (Framtida) Skärm för applikationsinställningar

3. components/
   - `__init__.py` - Gör mappen till ett Python-paket
   - `temperature_card.py` - Återanvändbar komponent för temperaturvisning på huvudskärmen
   - `dropdown_menu.py` - Navigationsskomponent för att växla mellan skärmar
   - `notification_toast.py` - Visuell komponent för att visa tillfälliga notifikationer i appen
   - `temperature_graph.py` - Grafkomponent som visar temperaturhistorik över tid

4. notifications/
   - `__init__.py` - Gör mappen till ett Python-paket
   - `notification_manager.py` - Hanterar visning och schemaläggning av notifikationer
   - `notification_service.py` - Affärslogik för att avgöra när och vilka notifikationer som ska skapas

5. services/
   - `__init__.py` - Gör mappen till ett Python-paket
   - `background_monitor.py` - Bakgrundstjänst som övervakar sensorer även när appen är minimerad
   - `platform_notifier.py` - Hanterar plattformsspecifika systemnotifikationer
   - `sound_manager.py` - Hanterar uppspelning av ljudnotifikationer

6. data/
   - `__init__.py` - Gör mappen till ett Python-paket
   - `data_manager.py` - Centraliserad datahanterings-klass som koordinerar datakällor
   - `data_provider.py` - Basklass för datakällor med gemensamt gränssnitt
   - `mock_data_provider.py` - Simulerar sensordata för utveckling och testning
   - `temperature_history.py` - Hanterar lagring och hämtning av temperaturhistorik

7. database/
   - `__init__.py` - Gör mappen till ett Python-paket
   - `db_manager.py` - Hanterar anslutningar till SQLite-databasen
   - `schema.py` - Definierar databasschema med tabeller för temperaturdata

8. models/
   - `__init__.py` - Gör mappen till ett Python-paket
   - `sensor_config.py` - Datamodell för sensorkonfiguration med gränsvärden och beteenden

## Beroenden

- Python 3.7+
- Kivy 2.0.0+
- KivyMD 2.0.1+
- kivy_garden.graph
- sqlite3 (ingår i Python standardbibliotek)

## Installation

1. Klona repot: `git clone [REPO_URL]`
2. Installera beroenden: `pip install -r requirements.txt`
3. Kör appen: `py main.py`
