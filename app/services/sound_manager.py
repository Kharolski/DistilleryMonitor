"""
SoundManager hanterar uppspelning av ljud för notifikationer.
"""

from kivy.core.audio import SoundLoader
import os

class SoundManager:
    """
    Hanterar ljuduppspelning för olika typer av notifikationer.
    """
    
    # Singleton-instans
    _instance = None
    
    @staticmethod
    def get_instance():
        """Returnerar singleton-instansen"""
        if SoundManager._instance is None:
            SoundManager._instance = SoundManager()
        return SoundManager._instance
    
    def __init__(self):
        """Initierar ljudhanteraren"""
        if SoundManager._instance is not None:
            raise RuntimeError("Försök att instansiera en ny SoundManager. Använd get_instance() istället.")
        
        # Ljudvolymer för olika typer (0.0 - 1.0)
        self.volume_levels = {
            'info': 0.3,
            'success': 0.5,
            'warning': 0.7,
            'critical': 1.0
        }
        
        # Ljudfiler för olika typer
        self.sounds = {}
        
        # Ladda ljud
        self._load_sounds()
    
    def _load_sounds(self):
        """Laddar ljudfiler"""
        base_path = self._get_sounds_path()
        
        # Definiera ljudfilerna och deras typer
        sound_files = {
            'info': 'notification.wav',
            'success': 'success.wav',
            'warning': 'warning.wav',
            'critical': 'alarm.wav'
        }
        
        # Ladda varje ljud
        for sound_type, filename in sound_files.items():
            file_path = os.path.join(base_path, filename)
            if os.path.exists(file_path):
                self.sounds[sound_type] = SoundLoader.load(file_path)
                # Sätt standardvolym
                if self.sounds[sound_type]:
                    self.sounds[sound_type].volume = self.volume_levels[sound_type]
            else:
                print(f"Varning: Ljudfil saknas - {file_path}")
    
    def _get_sounds_path(self):
        """Returnerar sökvägen till ljudfilerna"""
        # Basmapp för appen
        app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Sökväg till ljudmappen
        sounds_path = os.path.join(app_dir, 'assets', 'sounds')
        
        return sounds_path
    
    def play_sound(self, notification_type):
        """
        Spelar ett ljud baserat på notifikationstyp.
        
        Parametrar:
            notification_type (str): Typ av notifikation ('info', 'success', 'warning', 'critical')
        """
        sound_type = notification_type.lower()
        
        # Om ljudtypen inte stöds, använd info
        if sound_type not in self.sounds:
            sound_type = 'info'
        
        # Spela ljudet om det finns
        if sound_type in self.sounds and self.sounds[sound_type]:
            self.sounds[sound_type].play()
            print(f"Spelar ljud för notifikationstyp: {sound_type}")
        else:
            print(f"Kunde inte spela ljud för notifikationstyp: {sound_type}")
    
    def set_volume(self, notification_type, volume):
        """
        Sätter volymen för en viss notifikationstyp.
        
        Parametrar:
            notification_type (str): Typ av notifikation ('info', 'success', 'warning', 'critical')
            volume (float): Volym mellan 0.0 och 1.0
        """
        sound_type = notification_type.lower()
        
        # Begränsa volym till intervallet 0.0 - 1.0
        volume = max(0.0, min(1.0, volume))
        
        # Spara volyminstållning
        self.volume_levels[sound_type] = volume
        
        # Uppdatera volymen om ljudet är laddat
        if sound_type in self.sounds and self.sounds[sound_type]:
            self.sounds[sound_type].volume = volume
            print(f"Volym för {sound_type} satt till {volume}")