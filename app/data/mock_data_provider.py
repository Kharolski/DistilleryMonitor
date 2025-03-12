"""
MockDataProvider - Simulerar sensordata för testning.
"""

import random
from .data_provider import DataProvider

class MockDataProvider(DataProvider):
    """
    Implementering av DataProvider som genererar simulerad sensordata.
    Används för testning och utveckling innan riktiga sensorer är tillgängliga.
    """
    
    def __init__(self):
        """Initierar simulerat data"""
        # Grundtemperaturer som vi utgår från
        self.base_temps = {
            "PANNA": 85.5,      # Basnivå för pannan
            "KYLARE 1": 77.5,   # Basnivå för kylare 1
            "KYLARE 2": 75.3    # Basnivå för kylare 2
        }
        
        # Nuvarande temperaturer (kommer att variera runt basvärdena)
        self.current_temps = self.base_temps.copy()
        
        # Simuleringsparametrar för realistiska fluktuationer
        self.fluctuation_ranges = {
            "PANNA": (-2.0, 5.0),      # Pannan fluktuerar mer uppåt
            "KYLARE 1": (-1.0, 2.0),   # Kylare 1 har mindre fluktuationer
            "KYLARE 2": (-1.5, 1.5)    # Kylare 2 har symmetriska fluktuationer
        }
        
        # Uppdatera för att initiera med slumpmässiga värden
        self.update()
    
    def get_sensor_data(self):
        """Returnerar data för alla sensorer"""
        # Konvertera dictionary till lista med dictionarys
        return [{'name': name, 'temp': temp} for name, temp in self.current_temps.items()]
    
    def get_sensor_data_by_name(self, name):
        """Returnerar data för en specifik sensor"""
        if name in self.current_temps:
            return {'name': name, 'temp': self.current_temps[name]}
        return None
    
    def update(self):
        """
        Uppdaterar temperaturvärdena med realistiska fluktuationer.
        Metoden simulerar gradvisa temperaturförändringar runt basvärdena.
        """
        for name, base_temp in self.base_temps.items():
            # Hämta fluktuationsintervall för denna sensor
            min_fluct, max_fluct = self.fluctuation_ranges[name]
            
            # Beräkna ny temperatur baserat på bastemperatur och slumpmässig fluktuation
            # Vi använder också det nuvarande värdet för att skapa mer realistiska förändringar
            current = self.current_temps[name]
            
            # Tendens att röra sig tillbaka mot basvärdet om vi avviker för mycket
            if current < base_temp - 5:
                # För låg temperatur - tendens att öka
                fluct = random.uniform(0, max_fluct)
            elif current > base_temp + 5:
                # För hög temperatur - tendens att minska
                fluct = random.uniform(min_fluct, 0)
            else:
                # Inom normalområdet - slumpmässig fluktuation
                fluct = random.uniform(min_fluct, max_fluct)
            
            # Beräkna nytt värde med liten påverkan från fluktuation (mer realistiskt)
            # 80% av föregående värde + 20% av den nya fluktuationen
            new_temp = (current * 0.8) + ((base_temp + fluct) * 0.2)
            
            # Uppdatera den aktuella temperaturen
            self.current_temps[name] = round(new_temp, 1)
        
        return True
    
    def simulate_critical_conditions(self):
        """
        Simulerar kritiska förhållanden för test av larm/notifieringar.
        Sätter en av sensorerna till kritiskt högt värde.
        """
        # Välj en slumpmässig sensor
        sensor = random.choice(list(self.current_temps.keys()))
        
        # Hämta sensorns konfiguration för att bestämma kritiskt värde
        from models.sensor_config import SensorConfigs
        config = SensorConfigs.get_sensor_by_name(sensor)
        
        # Sätt värdet till strax över det kritiska tröskelvärdet
        critical_value = config.critical_threshold + random.uniform(1, 3)
        self.current_temps[sensor] = round(critical_value, 1)
        
        return sensor, self.current_temps[sensor]