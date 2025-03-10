from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from components.temperature_card import TemperatureCard

class HomeScreen(Screen):
    """
    Hemskärmen som visar alla temperatursensorer.
    """
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # Lägg till titel
        title = Label(
            text='Destillationsmonitor',
            font_size=dp(30),
            size_hint=(1, 0.15),
            bold=True
        )
        self.layout.add_widget(title)
        
        # Skapa container för korten
        self.cards_layout = BoxLayout(orientation='vertical', spacing=dp(20), size_hint=(1, 0.75))
        
        # Lägg till kort med mockdata
        self._add_mock_cards()
        
        self.layout.add_widget(self.cards_layout)
        
        # Uppdateringsknapp
        refresh_button = Button(
            text='Uppdatera',
            size_hint=(1, 0.1),
            background_color=(0.3, 0.5, 0.9, 1)
        )
        refresh_button.bind(on_press=self.refresh_data)
        self.layout.add_widget(refresh_button)
        
        self.add_widget(self.layout)
    
    def _add_mock_cards(self):
        """Lägg till kort med exempeldata för testning"""
        # Skapa och lägg till temperaturkort
        panna_card = TemperatureCard(name="PANNA", temp=78.5, optimal_range=(78, 82))
        kylare_card = TemperatureCard(name="KYLARE", temp=18.5, optimal_range=(15, 25))
        utlopp_card = TemperatureCard(name="UTLOPP", temp=25.3, optimal_range=(20, 35))
        
        self.cards_layout.add_widget(panna_card)
        self.cards_layout.add_widget(kylare_card)
        self.cards_layout.add_widget(utlopp_card)
    
    def refresh_data(self, instance):
        """Uppdatera data (kommer senare att hämta från API)"""
        # Rensa alla existerande kort
        self.cards_layout.clear_widgets()
        
        # Lägg till uppdaterade kort (för nu ändrar vi bara lite värden)
        import random
        
        panna_temp = 78.5 + random.uniform(-2, 2)
        kylare_temp = 18.5 + random.uniform(-5, 5)
        utlopp_temp = 25.3 + random.uniform(-3, 3)
        
        panna_card = TemperatureCard(name="PANNA", temp=panna_temp, optimal_range=(78, 82))
        kylare_card = TemperatureCard(name="KYLARE", temp=kylare_temp, optimal_range=(15, 25))
        utlopp_card = TemperatureCard(name="UTLOPP", temp=utlopp_temp, optimal_range=(20, 35))
        
        self.cards_layout.add_widget(panna_card)
        self.cards_layout.add_widget(kylare_card)
        self.cards_layout.add_widget(utlopp_card)
        