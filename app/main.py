from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.core.window import Window
from screens.home_screen import HomeScreen
from screens.detail_screen import DetailScreen
from screens.about_screen import AboutScreen

# Sätt app-storlek (viktigt för testning på dator)
Window.size = (400, 700)  # Typisk mobiltelefonsstorlek

# Viktigt: Ange fullscreen-läge för mobila enheter och hantera systemfältet bättre
# Window.softinput_mode = 'below_target'  # Håller input-fält synliga när tangentbordet visas
#Window.clearcolor = (0.95, 0.95, 0.95, 1)  # Ljusgrå bakgrund för hela appen

class DistilleryMonitorApp(App):
    """
    Huvudapplikationsklassen för Destillationsmonitorn.
    Denna klass ansvarar för att initiera appen och ladda dess konfiguration.
    """
    def build(self):
        """Bygg appens huvudlayout och returnera den"""
        # Skapa en screen manager med SlideTransition
        self.screen_manager = ScreenManager(transition=SlideTransition())
        
        # Lägg till våra skärmar
        home_screen = HomeScreen(name='home')
        detail_screen = DetailScreen(name='detail')
        about_screen = AboutScreen(name='about')
        
        self.screen_manager.add_widget(home_screen)
        self.screen_manager.add_widget(detail_screen)
        self.screen_manager.add_widget(about_screen)
        
        return self.screen_manager

if __name__ == '__main__':
    # Starta applikationen
    DistilleryMonitorApp().run()