"""
DataManager - Hanterar val och initiering av dataprovider.
"""

from .mock_data_provider import MockDataProvider

class DataManager:
    """
    Singleton-klass som hanterar dataproviders och tillhandahåller
    ett gemensamt gränssnitt för att interagera med dem.
    """
    
    # Singleton-instans
    _instance = None
    
    @staticmethod
    def get_instance():
        """Returnerar singleton-instansen av DataManager"""
        if DataManager._instance is None:
            DataManager._instance = DataManager()
        return DataManager._instance
    
    def __init__(self):
        """
        Initierar DataManager med lämplig dataprovider.
        För nu används MockDataProvider, men detta kommer att bytas ut senare.
        """
        if DataManager._instance is not None:
            raise RuntimeError("Försök att instansiera en ny DataManager. Använd get_instance() istället.")
        
        # Här väljer vi dataprovider - för tillfället använder vi mock-providern
        self.provider = MockDataProvider()
    
    def get_provider(self):
        """Returnerar den aktiva dataprovidern"""
        return self.provider
    
    def set_provider(self, provider):
        """
        Byter ut den aktiva dataprovidern.
        Används när vi vill byta från mock till verklig data.
        """
        self.provider = provider