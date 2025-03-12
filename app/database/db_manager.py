"""
Databashanterare för att hantera anslutning och operationer mot SQLite-databasen
"""

import os
import sqlite3
from . import schema

# Sökväg till databasen
# För Android kan det behöva ändras till plats som är tillgänglig för appen
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'temperature_app.db')

class DatabaseManager:
    """Hanterar alla databasoperationer"""
    
    @staticmethod
    def get_connection():
        """Skapa och returnera en anslutning till databasen"""
        conn = sqlite3.connect(DATABASE_PATH)
        # Aktivera foreign key support
        conn.execute("PRAGMA foreign_keys = ON")
        # Returnera rader som dictionaries istället för tuples
        conn.row_factory = sqlite3.Row
        return conn
    
    @staticmethod
    def initialize_database():
        """Skapa databasen och tabeller om de inte finns"""
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        
        # Skapa tabeller
        cursor.execute(schema.CREATE_TEMPERATURE_READINGS_TABLE)
        cursor.execute(schema.CREATE_SENSORS_TABLE)
        
        # Skapa versionstabell om den inte finns
        cursor.execute(schema.CREATE_VERSION_TABLE)
        
        # Kolla om versionstabellen är tom och initiera i så fall
        cursor.execute("SELECT COUNT(*) FROM db_version")
        if cursor.fetchone()[0] == 0:
            cursor.execute(schema.INITIALIZE_VERSION)
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def check_and_upgrade_database():
        """Kontrollerar databasversion och uppgraderar vid behov"""
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        
        # Hämta aktuell version
        cursor.execute(schema.GET_VERSION)
        current_version = cursor.fetchone()[0]
        
        # Exempel på uppgraderingslogik (lägg till när behov uppstår)
        # if current_version < 2:
        #     # cursor.execute("ALTER TABLE ... ")
        #     cursor.execute(schema.UPDATE_VERSION, (2,))
        
        conn.commit()
        conn.close()