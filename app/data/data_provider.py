"""
Abstrakt gränssnitt för dataproviders.
Denna modul definierar ett gemensamt gränssnitt för alla datakällor.
"""

from abc import ABC, abstractmethod

class DataProvider(ABC):
    """
    Abstrakt basklass för alla dataproviders.
    Definierar metoder som måste implementeras av alla konkreta providers.
    """
    
    @abstractmethod
    def get_sensor_data(self):
        """
        Hämtar data från alla sensorer.
        
        Returnerar:
            list: Lista med dictionarys innehållande sensordata.
                 Varje dictionary ska ha 'name' och 'temp' nycklar.
                 Exempel: [{'name': 'PANNA', 'temp': 85.5}, ...]
        """
        pass
    
    @abstractmethod
    def get_sensor_data_by_name(self, name):
        """
        Hämtar data för en specifik sensor baserat på namn.
        
        Parametrar:
            name (str): Namnet på sensorn att hämta.
            
        Returnerar:
            dict: Dictionary med sensordata. Ska ha 'name' och 'temp' nycklar.
                 Exempel: {'name': 'PANNA', 'temp': 85.5}
            None: Om sensorn inte hittas.
        """
        pass
    
    @abstractmethod
    def update(self):
        """
        Uppdaterar data från källan (t.ex. läser ny data från sensorer).
        
        Returnerar:
            bool: True om uppdateringen lyckades, annars False.
        """
        pass