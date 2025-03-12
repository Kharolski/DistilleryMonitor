"""
BackgroundMonitor hanterar övervakning av sensordata i bakgrunden.
"""

import threading
import time
from kivy.clock import Clock
from notifications.notification_manager import NotificationManager

class BackgroundMonitor:
    """
    Hanterar bakgrundsövervakning av sensordata.
    Körs i en separat tråd för att fortsätta övervakning
    även när appen är minimerad.
    """
    
    # Singleton-instans
    _instance = None
    
    @staticmethod
    def get_instance():
        """Returnerar singleton-instansen"""
        if BackgroundMonitor._instance is None:
            BackgroundMonitor._instance = BackgroundMonitor()
        return BackgroundMonitor._instance
    
    def __init__(self):
        """Initierar bakgrundsövervakaren"""
        if BackgroundMonitor._instance is not None:
            raise RuntimeError("Försök att instansiera en ny BackgroundMonitor. Använd get_instance() istället.")
        
        # Hämta data provider
        from data.data_manager import DataManager
        self.data_manager = DataManager.get_instance()
        self.data_provider = self.data_manager.get_provider()
        
        # Hämta notifikationshanterare
        self.notification_manager = NotificationManager.get_instance()
        
        # Flagga för att kontrollera om övervakning körs
        self.is_running = False
        
        # Tråden som kör övervakningen
        self.monitor_thread = None
        
        # Intervall mellan uppdateringar (i sekunder)
        self.update_interval = 5
    
    def start_monitoring(self):
        """Startar bakgrundsövervakningen"""
        if self.is_running:
            print("Bakgrundsövervakning körs redan")
            return
        
        self.is_running = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop)
        self.monitor_thread.daemon = True  # Tråden avslutas när huvudprogrammet avslutas
        self.monitor_thread.start()
        print("Bakgrundsövervakning startad")
    
    def stop_monitoring(self):
        """Stoppar bakgrundsövervakningen"""
        self.is_running = False
        if self.monitor_thread:
            # Tråden kommer att avslutas vid nästa kontroll av is_running
            self.monitor_thread = None
        print("Bakgrundsövervakning stoppad")
    
    def _monitoring_loop(self):
        """
        Huvudloopen för bakgrundsövervakning.
        Denna metod körs i en separat tråd.
        """
        while self.is_running:
            try:
                # Uppdatera data från provider
                self.data_provider.update()
                
                # Hämta uppdaterade sensordata
                sensor_data = self.data_provider.get_sensor_data()
                
                # Bearbeta varje sensor på huvudtråden via Clock
                for sensor in sensor_data:
                    # Använd lambda för att fånga värdena i en closure
                    sensor_name = sensor['name']
                    sensor_temp = sensor['temp']
                    
                    # Schemalägga processingen på huvudtråden
                    Clock.schedule_once(
                        lambda dt, name=sensor_name, temp=sensor_temp: 
                        self.notification_manager.process_sensor_update(name, temp), 
                        0
                    )
                
                # Vänta innan nästa uppdatering
                time.sleep(self.update_interval)
                
            except Exception as e:
                print(f"Fel i bakgrundsövervakning: {e}")
                # Fortsätt köra även vid fel
                time.sleep(self.update_interval)
    
    def set_update_interval(self, seconds):
        """Sätter intervallet mellan uppdateringar"""
        self.update_interval = seconds