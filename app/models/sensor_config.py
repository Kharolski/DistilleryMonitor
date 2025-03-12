"""
Sensorkonfigurationsmodell för destillationsprocessen.
Denna modul definierar temperaturintervall och tröskelvärden för de olika sensorerna.
"""

class SensorConfig:
    """Basklass för sensorkonfiguration"""
    
    def __init__(self, name, not_ready_range, optimal_range, warning_range, critical_threshold):
        """
        Initierar en sensorkonfiguration med de olika temperaturintervallen.
        
        Parametrar:
            name (str): Sensorns namn (t.ex. "PANNA")
            not_ready_range (tuple): Intervall för "inte färdigt" tillstånd (min, max)
            optimal_range (tuple): Intervall för optimal temperatur (min, max)
            warning_range (tuple): Intervall för varning (min, max)
            critical_threshold (float): Tröskelvärde för kritiskt tillstånd
        """
        self.name = name
        self.not_ready_range = not_ready_range
        self.optimal_range = optimal_range
        self.warning_range = warning_range
        self.critical_threshold = critical_threshold
    
    def get_status(self, temperature):
        """
        Bestämmer sensorns status baserat på temperaturvärdet.
        
        Parametrar:
            temperature (float): Aktuell temperatur
            
        Returnerar:
            str: En av statussträngarna "not_ready", "optimal", "warning", "critical"
        """
        if self.not_ready_range[0] <= temperature < self.not_ready_range[1]:
            return "not_ready"
        elif self.optimal_range[0] <= temperature <= self.optimal_range[1]:
            return "optimal"
        elif self.warning_range[0] <= temperature <= self.warning_range[1]:
            return "warning"
        elif temperature > self.critical_threshold:
            return "critical"
        else:
            # Om temperaturen är under not_ready_range[0], betrakta det som not_ready
            return "not_ready"
    
    def get_status_color(self, temperature):
        """
        Returnerar färgkoden för aktuell temperaturstatus.
        
        Parametrar:
            temperature (float): Aktuell temperatur
            
        Returnerar:
            tuple: RGBA-färgkod (0-1 för varje kanal)
        """
        status = self.get_status(temperature)
        
        if status == "not_ready":
            return (0.2, 0.6, 1.0, 1.0)  # Blå
        elif status == "optimal":
            return (0.2, 0.8, 0.2, 1.0)  # Grön
        elif status == "warning":
            return (1.0, 0.8, 0.0, 1.0)  # Gul
        elif status == "critical":
            return (1.0, 0.2, 0.2, 1.0)  # Röd
        else:
            return (0.5, 0.5, 0.5, 1.0)  # Grå (om något oväntat händer)
    
    def get_status_message(self, temperature):
        """
        Returnerar ett lämpligt meddelande baserat på temperaturstatus.
        
        Parametrar:
            temperature (float): Aktuell temperatur
            
        Returnerar:
            str: Ett beskrivande meddelande för aktuell status
        """
        status = self.get_status(temperature)
        
        if status == "not_ready":
            return f"Uppvärmning pågår. Målet är {self.optimal_range[0]}-{self.optimal_range[1]}°C."
        elif status == "optimal":
            return f"Optimal temperatur uppnådd!"
        elif status == "warning":
            return f"Varning: Temperaturen närmar sig kritisk nivå!"
        elif status == "critical":
            return f"KRITISKT: Temperaturen är för hög!"
        else:
            return "Temperaturen övervakas."


# Skapa specifika sensorkonfigurationer för de olika delarna av destillationsprocessen
class SensorConfigs:
    """Samling av alla sensorkonfigurationer i systemet"""
    
    @staticmethod
    def get_all_sensors():
        """Returnerar alla sensorkonfigurationer"""
        return [
            SensorConfigs.get_panna_config(),
            SensorConfigs.get_kylare1_config(),
            SensorConfigs.get_kylare2_config()
        ]
    
    @staticmethod
    def get_panna_config():
        """Konfiguration för pannsensorn"""
        return SensorConfig(
            name="PANNA",
            not_ready_range=(0, 78),      # Under 78°C är uppvärmningsfas
            optimal_range=(78, 89),       # 78-89°C är optimal temperatur
            warning_range=(89, 94),       # 89-94°C är varningszon
            critical_threshold=94         # Över 94°C är kritiskt
        )
    
    @staticmethod
    def get_kylare1_config():
        """Konfiguration för kylare 1-sensorn"""
        return SensorConfig(
            name="KYLARE 1",
            not_ready_range=(0, 76),      # Under 76°C är inte redo
            optimal_range=(76, 79),       # 76-79°C är optimal temperatur
            warning_range=(79, 80),       # 79-80°C är varningszon
            critical_threshold=80         # Över 80°C är kritiskt
        )
    
    @staticmethod
    def get_kylare2_config():
        """Konfiguration för kylare 2-sensorn"""
        return SensorConfig(
            name="KYLARE 2",
            not_ready_range=(0, 70),      # Under 70°C är inte redo
            optimal_range=(70, 80),       # 70-80°C är optimal temperatur
            warning_range=(80, 82),       # 80-82°C är varningszon
            critical_threshold=82         # Över 82°C är kritiskt
        )
    
    @staticmethod
    def get_sensor_by_name(name):
        """
        Hittar en sensorkonfiguration baserat på namn.
        
        Parametrar:
            name (str): Sensorns namn
            
        Returnerar:
            SensorConfig: Sensorkonfigurationen, eller None om den inte finns
        """
        for sensor in SensorConfigs.get_all_sensors():
            if sensor.name == name:
                return sensor
        return None