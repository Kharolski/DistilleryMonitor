"""
Hantera historik för temperaturmätningar
"""

import sqlite3
from datetime import datetime
from database.db_manager import DatabaseManager

class TemperatureHistory:
    """Klass för att hantera temperaturhistorik"""
    
    @staticmethod
    def add_temperature(sensor_name, temperature):
        """
        Lägg till en temperaturavläsning för en viss sensor
        
        Args:
            sensor_name (str): Namnet på sensorn
            temperature (float): Uppmätt temperatur
        """
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        
        # Skapa timestamp i ISO-format
        timestamp = datetime.now().isoformat()
        
        # Spara temperaturavläsning
        cursor.execute(
            "INSERT INTO temperature_readings (sensor_name, temperature, timestamp) VALUES (?, ?, ?)",
            (sensor_name, temperature, timestamp)
        )
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_history(sensor_name, limit=20):
        """
        Hämta senaste temperaturhistorik för en viss sensor
        
        Args:
            sensor_name (str): Namnet på sensorn
            limit (int): Maximalt antal mätvärden att hämta
            
        Returns:
            list: Lista med tupler innehållande (temperature, timestamp)
        """
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT temperature, timestamp FROM temperature_readings WHERE sensor_name = ? ORDER BY timestamp DESC LIMIT ?",
            (sensor_name, limit)
        )
        
        # Hämta alla rader
        rows = cursor.fetchall()
        
        # Konvertera till lista med tupler
        history = [(row['temperature'], row['timestamp']) for row in rows]
        
        conn.close()
        
        # Returnera i kronologisk ordning (äldst först)
        return list(reversed(history))
    
    @staticmethod
    def get_statistics(sensor_name, limit=20):
        """
        Beräkna statistik (min, max, medel) för en sensors temperaturhistorik
        
        Args:
            sensor_name (str): Namnet på sensorn
            limit (int): Antal mätvärden att inkludera i statistiken
            
        Returns:
            dict: Innehåller min_temp, max_temp, avg_temp
        """
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT MIN(temperature) as min_temp, MAX(temperature) as max_temp, AVG(temperature) as avg_temp FROM "
            "(SELECT temperature FROM temperature_readings WHERE sensor_name = ? ORDER BY timestamp DESC LIMIT ?)",
            (sensor_name, limit)
        )
        
        row = cursor.fetchone()
        
        conn.close()
        
        if row and row['min_temp'] is not None:
            return {
                'min_temp': row['min_temp'],
                'max_temp': row['max_temp'],
                'avg_temp': row['avg_temp']
            }
        else:
            return {
                'min_temp': 0,
                'max_temp': 0,
                'avg_temp': 0
            }

     # TEST DATA   
    @staticmethod
    def add_temperature_with_timestamp(sensor_name, temperature, timestamp):
        """Lägg till temperatur med angivet timestamp (för testdata)"""
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO temperature_readings (sensor_name, temperature, timestamp) VALUES (?, ?, ?)",
            (sensor_name, temperature, timestamp)
        )
        
        conn.commit()
        conn.close()