"""
NotificationService hanterar skapande och spårning av notifikationer.
"""

import time
from models.sensor_config import SensorConfigs

class Notification:
    """
    Representerar en enskild notifikation.
    """
    
    # Notifikationstyper
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    CRITICAL = "critical"
    
    def __init__(self, message, notification_type, sensor_name=None, temp=None):
        """
        Initierar en notifikation.
        
        Parametrar:
            message (str): Notifikationsmeddelandet
            notification_type (str): Typ av notifikation (INFO, SUCCESS, WARNING, CRITICAL)
            sensor_name (str, optional): Namnet på sensorn som genererade notifikationen
            temp (float, optional): Temperaturvärdet som orsakade notifikationen
        """
        self.message = message
        self.type = notification_type
        self.timestamp = time.time()
        self.sensor_name = sensor_name
        self.temp = temp
    
    def get_formatted_time(self):
        """Returnerar en formaterad tidsangivelse för notifikationen"""
        return time.strftime('%H:%M:%S', time.localtime(self.timestamp))
    
    def get_color(self):
        """Returnerar färg baserat på notifikationstyp"""
        if self.type == self.INFO:
            return (0.2, 0.6, 1.0, 1.0)  # Blå
        elif self.type == self.SUCCESS:
            return (0.2, 0.8, 0.2, 1.0)  # Grön
        elif self.type == self.WARNING:
            return (1.0, 0.8, 0.0, 1.0)  # Gul
        elif self.type == self.CRITICAL:
            return (1.0, 0.2, 0.2, 1.0)  # Röd
        else:
            return (0.7, 0.7, 0.7, 1.0)  # Grå
        
    def get_type_name(self):
        """Returnerar notifikationstypen som sträng"""
        type_map = {
            self.INFO: "info",
            self.SUCCESS: "success",
            self.WARNING: "warning",
            self.CRITICAL: "critical"
        }
        return type_map.get(self.type, "info")

class NotificationService:
    """
    Service för att hantera notifikationer. Denna klass:
    - Spårar sensorer och deras status
    - Genererar notifikationer när status ändras
    - Lagrar notifikationshistorik
    """
    
    # Singleton-instans
    _instance = None
    
    @staticmethod
    def get_instance():
        """Returnerar singleton-instansen"""
        if NotificationService._instance is None:
            NotificationService._instance = NotificationService()
        return NotificationService._instance
    
    def __init__(self):
        """Initierar notifikationsservicen"""
        if NotificationService._instance is not None:
            raise RuntimeError("Försök att instansiera en ny NotificationService. Använd get_instance() istället.")
        
        # Lagra tidigare status för alla sensorer
        self.previous_statuses = {}
        
        # Lista över tidigare notifikationer
        self.notification_history = []
        
        # Callbackfunktion för att visa notifikationer
        self.notification_callback = None
    
    def set_notification_callback(self, callback):
        """
        Sätter callbackfunktionen som anropas för att visa en notifikation.
        
        Parametrar:
            callback (function): Funktion som tar emot en Notification som parameter
        """
        self.notification_callback = callback
    
    def process_sensor_data(self, name, temp):
        """
        Behandlar ny sensordata, jämför med tidigare status och genererar notifikationer vid behov.
        
        Parametrar:
            name (str): Sensorns namn
            temp (float): Aktuell temperatur
            
        Returnerar:
            Notification or None: En ny notifikation om statusen ändrades, annars None
        """
        # Hämta sensorkonfiguration
        sensor_config = SensorConfigs.get_sensor_by_name(name)
        if not sensor_config:
            return None
        
        # Bestäm nuvarande status
        current_status = sensor_config.get_status(temp)
        
        # Om detta är första gången vi ser sensorn, spara bara statusen
        if name not in self.previous_statuses:
            self.previous_statuses[name] = current_status
            return None
        
        # Hämta tidigare status
        previous_status = self.previous_statuses[name]
        
        # Kontrollera om statusen ändrats
        if current_status != previous_status:
            # Skapa lämplig notifikation baserat på statusövergång
            notification = self._create_notification_for_transition(
                name, temp, previous_status, current_status, sensor_config)
            
            # Uppdatera tidigare status
            self.previous_statuses[name] = current_status
            
            # Om vi har en notifikation och en callback, anropa den
            if notification and self.notification_callback:
                self.notification_callback(notification)
                
                # Lägg till i historiken
                self.notification_history.append(notification)
                
                # Begränsa historiken till 100 notifikationer
                if len(self.notification_history) > 100:
                    self.notification_history.pop(0)
                
                return notification
        
        return None
    
    def _create_notification_for_transition(self, name, temp, prev_status, curr_status, sensor_config):
        """
        Skapar en lämplig notifikation baserat på statusövergång.
        
        Parametrar:
            name (str): Sensorns namn
            temp (float): Aktuell temperatur
            prev_status (str): Tidigare status
            curr_status (str): Nuvarande status
            sensor_config (SensorConfig): Sensorkonfigurationen
            
        Returnerar:
            Notification: En ny notifikation, eller None om ingen notifikation behövs
        """
        message = None
        notification_type = Notification.INFO
        
        # Från inte färdig till optimal
        if prev_status == "not_ready" and curr_status == "optimal":
            message = f"{name} har nått optimal temperatur ({temp:.1f}°C)"
            notification_type = Notification.SUCCESS
        
        # Från optimal till varning
        elif prev_status == "optimal" and curr_status == "warning":
            message = f"Varning: {name} närmar sig kritisk nivå ({temp:.1f}°C)"
            notification_type = Notification.WARNING
        
        # Från varning till kritisk
        elif prev_status in ["optimal", "warning"] and curr_status == "critical":
            message = f"KRITISKT: {name} har överskridit säker nivå ({temp:.1f}°C)!"
            notification_type = Notification.CRITICAL
        
        # Återgång till optimal från varning eller kritisk
        elif prev_status in ["warning", "critical"] and curr_status == "optimal":
            message = f"{name} har återgått till optimal nivå ({temp:.1f}°C)"
            notification_type = Notification.SUCCESS
            
        # Återgång till varning från kritisk
        elif prev_status == "critical" and curr_status == "warning":
            message = f"{name} har sjunkit från kritisk nivå, fortfarande varning ({temp:.1f}°C)"
            notification_type = Notification.WARNING
        
        # Om vi har ett meddelande, skapa notifikation
        if message:
            return Notification(message, notification_type, name, temp)
        
        return None
    
    def get_notification_history(self):
        """Returnerar notifikationshistoriken"""
        return self.notification_history