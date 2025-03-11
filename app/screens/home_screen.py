from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from components.temperature_card import TemperatureCard
from components.dropdown_menu import DropDownMenu

class HomeScreen(Screen):
    """
    Hemskärmen som visar alla temperatursensorer.
    """
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        
        # Huvudlayout - inga scrollbara delar här
        self.layout = BoxLayout(orientation='vertical', spacing=dp(3))
        
        # Header-sektion med meny - denna del är "sticky"
        self.header = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(50))
        
        # Lägg till dropdown-meny i headern
        self.dropdown_menu = DropDownMenu()
        self.header.add_widget(self.dropdown_menu)
        
        # Lägg till headern i huvudlayouten
        self.layout.add_widget(self.header)
        
        # Liten padding mellan header och scrollbart innehåll
        padding_box = BoxLayout(size_hint=(1, None), height=dp(0))
        self.layout.add_widget(padding_box)
        
        # Skapar en scrollbar för innehållet (korten)
        self.scroll_view = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            do_scroll_y=True
        )
        
        # Container för det scrollbara innehållet
        self.scrollable_content = BoxLayout(
            orientation='vertical', 
            spacing=dp(20),
            size_hint=(1, None),  # Viktig för scrollning
            padding=dp(10)
        )
        
        # Skapa container för korten
        self.cards_layout = BoxLayout(
            orientation='vertical', 
            spacing=dp(20), 
            size_hint=(1, None),  # Viktig för scrollning
            height=dp(400)  # Justerat eftersom vi har färre kort
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
        
        # Uppdateringsknapp - ligger utanför scrollbara området
        refresh_button = Button(
            text='Uppdatera',
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.3, 0.5, 0.9, 1)
        )
        refresh_button.bind(on_press=self.refresh_data)
        self.layout.add_widget(refresh_button)
        
        self.add_widget(self.layout)
    
    def on_enter(self):
        """Anropas när skärmen visas - säkerställer att vi har manager tillgänglig"""
        # Sätt screen_manager för dropdown-menyn
        self.dropdown_menu.screen_manager = self.manager
        self._add_mock_cards()
    
    def _add_mock_cards(self):
        """Lägg till kort med exempeldata för testning"""
        # Rensa befintliga kort först
        self.cards_layout.clear_widgets()
        
        # Skapa och lägg till temperaturkort
        panna_card = TemperatureCard(name="PANNA", temp=78.5, optimal_range=(78, 82))
        kylare_card = TemperatureCard(name="KYLARE", temp=18.5, optimal_range=(15, 25))
        utlopp_card = TemperatureCard(name="UTLOPP", temp=25.3, optimal_range=(20, 35))
        
        # Bind klickhändelser
        panna_card.bind(on_release=self.on_panna_press)
        kylare_card.bind(on_release=self.on_kylare_press)
        utlopp_card.bind(on_release=self.on_utlopp_press)
        
        # Lägg till korten
        self.cards_layout.add_widget(panna_card)
        self.cards_layout.add_widget(kylare_card)
        self.cards_layout.add_widget(utlopp_card)
        
        # Uppdatera höjden på cards_layout för att få korrekt scrollning
        total_height = sum(card.height + dp(13) for card in [panna_card, kylare_card, utlopp_card])
        self.cards_layout.height = total_height

    # Resten av metoderna är oförändrade
    def on_panna_press(self, instance):
        self.show_details("PANNA", 78.5, (78, 82))
        
    def on_kylare_press(self, instance):
        self.show_details("KYLARE", 18.5, (15, 25))
        
    def on_utlopp_press(self, instance):
        self.show_details("UTLOPP", 25.3, (20, 35))
    
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
        
        # Bind klickhändelser
        panna_card.bind(on_release=lambda x: self.show_details("PANNA", panna_temp, (78, 82)))
        kylare_card.bind(on_release=lambda x: self.show_details("KYLARE", kylare_temp, (15, 25)))
        utlopp_card.bind(on_release=lambda x: self.show_details("UTLOPP", utlopp_temp, (20, 35)))
        
        # Lägg till korten
        self.cards_layout.add_widget(panna_card)
        self.cards_layout.add_widget(kylare_card)
        self.cards_layout.add_widget(utlopp_card)
        
        # Uppdatera höjden på cards_layout
        total_height = sum(card.height + dp(20) for card in [panna_card, kylare_card, utlopp_card])
        self.cards_layout.height = total_height
    
    def show_details(self, name, temp, optimal_range):
        """Visa detaljskärmen för en sensor"""
        try:
            # Hämta detaljskärmen från screen manager
            detail_screen = self.manager.get_screen('detail')
            
            # Sätt aktuell sensor och dess data
            detail_screen.set_sensor(name, temp, optimal_range)
            
            # Sätt animationsriktning till vänster
            self.manager.transition.direction = 'left'
            
            # Byt till detaljskärmen
            self.manager.current = 'detail'
        except Exception as e:
            # Behåll en enkel felhantering för att fånga allvarliga problem
            print(f"Error navigating to detail screen: {e}")