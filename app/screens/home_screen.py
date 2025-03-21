from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle

from components.temperature_card import TemperatureCard
from components.dropdown_menu import DropDownMenu
from notifications.notification_manager import NotificationManager

class HomeScreen(MDScreen):
    """
    Hemskärmen som visar alla temperatursensorer.
    """
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        # Initialisera DataManager och hämta provider
        from data.data_manager import DataManager
        self.data_manager = DataManager.get_instance()
        self.data_provider = self.data_manager.get_provider()
        
        # Huvudlayout - inga scrollbara delar här
        self.layout = MDBoxLayout(
            orientation='vertical', 
            spacing=dp(3),
            theme_bg_color="Custom",
            md_bg_color=[0.2, 0.2, 0.2, 1]  # bakgrund
        )
        
        # Header-sektion med meny - denna del är "sticky"
        self.header = MDBoxLayout(
            orientation='vertical', 
            size_hint=(1, None), 
            height=dp(50),
            theme_bg_color="Custom",
            md_bg_color=[0, 0, 0, 0]  # bakgrund för header
        )
        
        # Lägg till dropdown-meny i headern
        self.dropdown_menu = DropDownMenu()
        self.header.add_widget(self.dropdown_menu)
        
        # Lägg till headern i huvudlayouten
        self.layout.add_widget(self.header)
        
        # Skapar en scrollbar för innehållet (korten)
        self.scroll_view = MDScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            do_scroll_y=True,
            bar_color=[0.7, 0.7, 0.7, 0.8],  # Ljusgrå scrollbar
            bar_width=dp(4)  # Lite bredare scrollbar för bättre synlighet
        )
        
        # Container för det scrollbara innehållet
        self.scrollable_content = MDBoxLayout(
            orientation='vertical', 
            spacing=dp(0),
            size_hint=(1, None),  # Viktig för scrollning
            padding=dp(10),
            md_bg_color=[0, 0, 0, 0]  # bakgrund
        )
        
        # Skapa container för korten
        self.cards_layout = MDBoxLayout(
            orientation='vertical', 
            spacing=dp(10),
            size_hint=(1, None),  # Viktig för scrollning
            height=dp(350),  # Justerat eftersom vi har färre kort
            md_bg_color=[0, 0, 0, 0]  # bakgrund
        )
        
        # Lägg till cards_layout till scrollable_content
        self.scrollable_content.add_widget(self.cards_layout)
        
        # Bind height för att få korrekt scrollning
        self.cards_layout.bind(minimum_height=self.cards_layout.setter('height'))
        self.scrollable_content.bind(minimum_height=self.scrollable_content.setter('height'))
        
        # Lägg till scrollable_content till scroll_view
        self.scroll_view.add_widget(self.scrollable_content)
        
        # Lägg till scroll_view till huvudlayouten
        self.layout.add_widget(self.scroll_view)
        
        # Knappcontainer för bättre layout - ändrad till horisontell orientering
        button_container = MDBoxLayout(
            orientation='horizontal',  # Ändrad från 'vertical' till 'horizontal'
            spacing=dp(10),  # Ökat mellanrum mellan knapparna
            padding=[dp(10), dp(5), dp(10), dp(10)],
            size_hint=(1, None),
            height=dp(54),  # Minskad höjd eftersom knapparna nu är bredvid varandra
            md_bg_color=[0.2, 0.2, 0.2, 1]  # bakgrund
        )
        
        # Uppdateringsknapp - ligger utanför scrollbara området
        refresh_button = MDButton(
            MDButtonText(
                text='Uppdatera',
            ),
            style="filled",  # Lägg till stil
            size_hint=(0.5, None),
            height=dp(40),
            theme_bg_color="Custom",
            md_bg_color=[0.2, 0.4, 0.6, 1],  # Blå knapp
        )
        refresh_button.bind(on_press=self.refresh_data)
        button_container.add_widget(refresh_button)

        # Knapp för att simulera kritiska förhållanden (för testning)
        test_button = MDButton(
            MDButtonText(
                text="Simulera Kritisk",
            ),
            style="filled",  # Lägg till stil
            size_hint=(0.5, None),
            height=dp(40),
            theme_bg_color="Custom",
            md_bg_color=[0.8, 0.2, 0.2, 1],  # Röd knapp
        )
        test_button.bind(on_release=self.simulate_critical)
        button_container.add_widget(test_button)
        
        # Lägg till knappcontainern till huvudlayouten
        self.layout.add_widget(button_container)
        
        self.add_widget(self.layout)
    
    def on_enter(self):
        """Anropas när skärmen visas - säkerställer att vi har manager tillgänglig"""
        # Sätt screen_manager för dropdown-menyn
        self.dropdown_menu.screen_manager = self.manager
        self._add_mock_cards()
    
    def _add_mock_cards(self):
        """Lägg till kort baserat på data från providern"""
        # Rensa befintliga kort först
        self.cards_layout.clear_widgets()
        
        # Hämta data från providern
        sensor_data = self.data_provider.get_sensor_data()
        
        # Lista för att hålla korten
        cards = []
        
        # Skapa kort för varje sensor
        for sensor in sensor_data:
            card = TemperatureCard(name=sensor['name'], temp=sensor['temp'])
            card.bind(on_release=lambda x, sensor_name=sensor['name'], sensor_temp=sensor['temp']: 
                    self.show_details(sensor_name, sensor_temp))
            cards.append(card)
            self.cards_layout.add_widget(card)
        
        # Uppdatera höjden på cards_layout för att få korrekt scrollning
        total_height = sum(card.height + dp(7) for card in cards)
        self.cards_layout.height = total_height

    def on_panna_press(self, instance):
        self.show_details("PANNA", 78.5, (78, 82))
        
    def on_kylare_press(self, instance):
        self.show_details("KYLARE", 18.5, (15, 25))
        
    def on_utlopp_press(self, instance):
        self.show_details("UTLOPP", 25.3, (20, 35))
    
    def refresh_data(self, instance):
        """Uppdatera data från providern"""
        # Uppdatera provider för att hämta ny data
        self.data_provider.update()
        
        # Hämta uppdaterade sensordata
        sensor_data = self.data_provider.get_sensor_data()
        
        # Få åtkomst till notifikationshanteraren
        notification_manager = NotificationManager.get_instance()
        
        # Bearbeta varje sensor för eventuella notifikationer
        for sensor in sensor_data:
            notification_manager.process_sensor_update(sensor['name'], sensor['temp'])
        
        # Lägg till uppdaterade kort
        self._add_mock_cards()
    
    def show_details(self, name, temp):
        """Visa detaljskärmen för en sensor"""
        try:
            # Hämta detaljskärmen från screen manager
            detail_screen = self.manager.get_screen('detail')
            
            # Sätt aktuell sensor och dess data - nu använder vi SensorConfig
            detail_screen.set_sensor(name, temp)
            
            # Sätt animationsriktning till vänster
            self.manager.transition.direction = 'left'
            
            # Byt till detaljskärmen
            self.manager.current = 'detail'
        except Exception as e:
            # Behåll en enkel felhantering för att fånga allvarliga problem
            print(f"Error navigating to detail screen: {e}")

    # Test metoden:
    def simulate_critical(self, instance):
        """Simulerar en kritisk temperatur för testning av notifikationer"""
        sensor, temp = self.data_provider.simulate_critical_conditions()
        
        # Meddela notifikationssystemet
        notification_manager = NotificationManager.get_instance()
        notification_manager.process_sensor_update(sensor, temp)
        
        # Uppdatera korten
        self._add_mock_cards()
