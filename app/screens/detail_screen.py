from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle

class DetailScreen(Screen):
    """
    Skärm som visar detaljerad information om en temperaturgivare.
    """
    
    def __init__(self, **kwargs):
        super(DetailScreen, self).__init__(**kwargs)
        
        # Initiera huvudvariabler
        self.sensor_name = ""
        self.temperature = 0.0
        self.sensor_config = None
        
        # Skapa huvudlayout
        main_layout = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(10)
        )
        
        # Skapa header med tillbakaknapp
        header = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.1),
            spacing=dp(10)
        )
        
        # Tillbakaknapp
        back_button = Button(
            text="Tillbaka",
            size_hint=(0.3, 1),
            background_normal='',
            background_color=(0.3, 0.4, 0.5, 1)
        )
        back_button.bind(on_release=self.go_back)
        header.add_widget(back_button)
        
        # Titel för skärmen
        self.title_label = Label(
            text="Sensor Details",
            font_size=dp(20),
            bold=True,
            size_hint=(0.7, 1)
        )
        header.add_widget(self.title_label)
        
        # Lägg till header till huvudlayout
        main_layout.add_widget(header)
        
        # Innehållslayout
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            size_hint=(1, 0.9)
        )
        
        # Temperaturvisning
        temp_box = BoxLayout(
            orientation='vertical',
            spacing=dp(5),
            size_hint=(1, 0.3)
        )
        
        temp_header = Label(
            text="Aktuell temperatur",
            font_size=dp(16),
            size_hint=(1, 0.3)
        )
        temp_box.add_widget(temp_header)
        
        self.temp_label = Label(
            text="--°C",
            font_size=dp(40),
            bold=True,
            size_hint=(1, 0.7)
        )
        temp_box.add_widget(self.temp_label)
        
        content.add_widget(temp_box)
        
        # Status
        status_box = BoxLayout(
            orientation='vertical',
            spacing=dp(5),
            size_hint=(1, 0.2)
        )
        
        status_header = Label(
            text="Status",
            font_size=dp(16),
            size_hint=(1, 0.4)
        )
        status_box.add_widget(status_header)
        
        self.status_label = Label(
            text="--",
            font_size=dp(24),
            bold=True,
            size_hint=(1, 0.6)
        )
        status_box.add_widget(self.status_label)
        
        content.add_widget(status_box)
        
        # Meddelande
        message_box = BoxLayout(
            orientation='vertical',
            spacing=dp(5),
            size_hint=(1, 0.2)
        )
        
        self.message_label = Label(
            text="Ingen information tillgänglig",
            font_size=dp(16),
            size_hint=(1, 1),
            halign='center',
            valign='middle'
        )
        # Aktivera radbrytning för meddelandet
        self.message_label.bind(size=lambda *args: setattr(self.message_label, 'text_size', (self.message_label.width, None)))
        
        message_box.add_widget(self.message_label)
        content.add_widget(message_box)
        
        # Optimal temperaturintervall
        optimal_box = BoxLayout(
            orientation='vertical',
            spacing=dp(5),
            size_hint=(1, 0.2)
        )
        
        self.optimal_label = Label(
            text="Optimalt intervall: --",
            font_size=dp(16),
            size_hint=(1, 1)
        )
        optimal_box.add_widget(self.optimal_label)
        
        content.add_widget(optimal_box)
        
        # Plats för framtida grafik/diagram
        graph_placeholder = BoxLayout(
            size_hint=(1, 0.3)
        )
        
        graph_text = Label(
            text="[Temperaturgrafer kommer här]",
            italic=True,
            color=(0.5, 0.5, 0.5, 1)
        )
        graph_placeholder.add_widget(graph_text)
        
        content.add_widget(graph_placeholder)
        
        # Lägg till innehållet till huvudlayout
        main_layout.add_widget(content)
        
        # Lägg till huvudlayout till skärmen
        self.add_widget(main_layout)
    
    def set_sensor(self, name, temp):
        """
        Sätt aktuell sensor och dess data
        """
        self.sensor_name = name
        self.temperature = temp
        
        # Hämta sensorkonfiguration
        from models.sensor_config import SensorConfigs
        self.sensor_config = SensorConfigs.get_sensor_by_name(name)
        
        # Uppdatera UI-elementen
        self.title_label.text = f"{name} Details"
        self.temp_label.text = f"{temp:.1f}°C"
        
        # Sätt status och färg
        status = self.sensor_config.get_status(temp)
        status_color = self.sensor_config.get_status_color(temp)
        status_message = self.sensor_config.get_status_message(temp)
        
        # Uppdatera status-relaterade UI-element
        self.status_label.text = status.upper()
        self.status_label.color = status_color
        self.message_label.text = status_message
        
        # Uppdatera optimal range
        self.optimal_label.text = f"Optimalt intervall: {self.sensor_config.optimal_range[0]}-{self.sensor_config.optimal_range[1]}°C"
    
    def go_back(self, instance):
        """
        Navigera tillbaka till huvudskärmen
        """
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'