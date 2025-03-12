"""
Schema och SQL-definitioner för databas
"""

# Skapa temperature_readings tabell
CREATE_TEMPERATURE_READINGS_TABLE = """
CREATE TABLE IF NOT EXISTS temperature_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_name TEXT NOT NULL,
    temperature REAL NOT NULL,
    timestamp TEXT NOT NULL
);
"""

# Skapa sensorkonfigurationstabell
CREATE_SENSORS_TABLE = """
CREATE TABLE IF NOT EXISTS sensors (
    name TEXT PRIMARY KEY,
    min_optimal REAL,
    max_optimal REAL,
    warning_low REAL,
    warning_high REAL,
    critical_low REAL, 
    critical_high REAL
);
"""

# Skapa versionstabell för databasmigreringar
CREATE_VERSION_TABLE = """
CREATE TABLE IF NOT EXISTS db_version (
    version INTEGER
);
"""

# Initiera versionsnummer om tabellen är nyligen skapad
INITIALIZE_VERSION = """
INSERT INTO db_version (version) VALUES (1);
"""

# Hämta aktuell version
GET_VERSION = """
SELECT version FROM db_version;
"""

# För att uppdatera versionen vid migrering
UPDATE_VERSION = """
UPDATE db_version SET version = ?;
"""