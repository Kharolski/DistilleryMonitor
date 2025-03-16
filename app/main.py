from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.core.window import Window
from kivymd.uix.floatlayout import MDFloatLayout

from screens.home_screen import HomeScreen
from screens.detail_screen import DetailScreen
from screens.about_screen import AboutScreen
from notifications.notification_manager import NotificationManager
from services.background_monitor import BackgroundMonitor
from database.db_manager import DatabaseManager

# Initiera databasen
DatabaseManager.initialize_database()
DatabaseManager.check_and_upgrade_database()

# Generera testdata för först körning
from data.mock_data_provider import MockDataProvider
mock_provider = MockDataProvider()
mock_provider.generate_test_history()

# Sätt app-storlek (viktigt för testning på dator)
Window.size = (400, 700)  # Typisk mobiltelefonsstorlek

class DistilleryMonitorApp(MDApp):
    """
    Huvudapplikationsklassen för Destillationsmonitorn.
    Denna klass ansvarar för att initiera appen och ladda dess konfiguration.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ställ in appens tema
        self.theme_cls.primary_palette = "Blue"  # Huvudfärg
        self.theme_cls.accent_palette = "Amber"  # Accentfärg
        self.theme_cls.theme_style = "Light"     # Ljust eller mörkt tema
        
        # Ställ in appnamnet (visas i titelraden)
        self.title = "Destillationsmonitor"
    
    def build(self):
        """Bygg appens huvudlayout och returnera den"""
        # Skapa en root layout som kan innehålla både ScreenManager och notifikationer
        # Använd MDFloatLayout istället för FloatLayout
        self.root_layout = MDFloatLayout()
        
        # Skapa en screen manager med SlideTransition
        self.screen_manager = ScreenManager(transition=SlideTransition())
        self.screen_manager.size_hint = (1, 1)  # Ta upp hela utrymmet
        
        # Lägg till våra skärmar
        home_screen = HomeScreen(name='home')
        detail_screen = DetailScreen(name='detail')
        about_screen = AboutScreen(name='about')
        
        self.screen_manager.add_widget(home_screen)
        self.screen_manager.add_widget(detail_screen)
        self.screen_manager.add_widget(about_screen)
        
        # Lägg till screen_manager till root_layout
        self.root_layout.add_widget(self.screen_manager)
        
        # Initiera notifikationshanteraren och ge den tillgång till root_layout
        notification_manager = NotificationManager.get_instance()
        notification_manager.set_app_root(self.root_layout)

        # Initiera och starta bakgrundsövervakning
        background_monitor = BackgroundMonitor.get_instance()
        background_monitor.start_monitoring()
        
        return self.root_layout

if __name__ == '__main__':
    # Starta applikationen
    DistilleryMonitorApp().run()