from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from screens.home_screen import HomeScreen

# Sätt app-storlek (viktigt för testning på dator)
Window.size = (400, 700)  # Typisk mobiltelefonsstorlek

class DistilleryMonitorApp(App):
    """
    Huvudapplikationsklassen för Destillationsmonitorn.
    Denna klass ansvarar för att initiera appen och ladda dess konfiguration.
    """
    def build(self):
        """Bygg appens huvudlayout och returnera den"""
        # Skapa en screen manager för att hantera olika skärmar
        self.screen_manager = ScreenManager()
        
        # Lägg till vår hemskärm
        home_screen = HomeScreen(name='home')
        self.screen_manager.add_widget(home_screen)
        
        return self.screen_manager

if __name__ == '__main__':
    # Starta applikationen
    DistilleryMonitorApp().run()