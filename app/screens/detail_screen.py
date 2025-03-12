from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from components.temperature_graph import TemperatureGraph
from data.temperature_history import TemperatureHistory
from kivy.clock import Clock

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
            padding=dp(15),  # Minska padding för mer kompakt layout
            spacing=dp(8)    # Minska spacing
        )
        
        # Titel för skärmen
        title_container = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.08),  # Minska höjden för en mer kompakt layout
            padding=[0, 0, 0, dp(5)]  # Lägg till lite padding i botten
        )
        
        self.title_label = Label(
            text="Sensor Details",
            font_size=dp(22),
            bold=True,
            size_hint=(1, 1),
            halign='center'
        )
        self.title_label.bind(size=lambda *args: setattr(self.title_label, 'text_size', (self.title_label.width, None)))
        
        title_container.add_widget(self.title_label)
        main_layout.add_widget(title_container)
        
        # Innehållslayout
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(0),  # Ingen standardspacing - vi styr detta individuellt
            size_hint=(1, 0.84)
        )

        # Temperaturvisning
        temp_box = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint=(1, 0.1)  # Minska höjden
        )

        temp_header = Label(
            text="Aktuell temperatur:",
            font_size=dp(16),
            size_hint=(0.5, 1),
            halign='right',
            valign='middle'
        )
        temp_header.bind(size=lambda *args: setattr(temp_header, 'text_size', (temp_header.width, temp_header.height)))
        temp_box.add_widget(temp_header)

        self.temp_label = Label(
            text="--°C",
            font_size=dp(32),
            bold=True,
            size_hint=(0.5, 1),
            halign='left',
            valign='middle'
        )
        self.temp_label.bind(size=lambda *args: setattr(self.temp_label, 'text_size', (self.temp_label.width, self.temp_label.height)))
        temp_box.add_widget(self.temp_label)

        content.add_widget(temp_box)

        # Optimal temperaturintervall - direkt under temperatur utan mellanrum
        optimal_box = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint=(1, 0.1),  # Minska höjden
            padding=[0, 0, 0, 0]  # Ingen padding
        )

        optimal_header = Label(
            text="Optimalt intervall:",
            font_size=dp(16),
            size_hint=(0.5, 1),
            halign='right',
            valign='middle'
        )
        optimal_header.bind(size=lambda *args: setattr(optimal_header, 'text_size', (optimal_header.width, optimal_header.height)))
        optimal_box.add_widget(optimal_header)

        self.optimal_label = Label(
            text="--",
            font_size=dp(16),
            size_hint=(0.5, 1),
            halign='left',
            valign='middle'
        )
        self.optimal_label.bind(size=lambda *args: setattr(self.optimal_label, 'text_size', (self.optimal_label.width, self.optimal_label.height)))
        optimal_box.add_widget(self.optimal_label)

        content.add_widget(optimal_box)

        # Lägg till mellanrum mellan temperatur och status
        from kivy.uix.widget import Widget
        content.add_widget(Widget(size_hint_y=0.03))  # Mellanrum

        # Status
        status_box = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint=(1, 0.1)  # Minska höjden
        )

        status_header = Label(
            text="Status:",
            font_size=dp(16),
            size_hint=(0.5, 1),
            halign='right',
            valign='middle'
        )
        status_header.bind(size=lambda *args: setattr(status_header, 'text_size', (status_header.width, status_header.height)))
        status_box.add_widget(status_header)

        self.status_label = Label(
            text="--",
            font_size=dp(20),
            bold=True,
            size_hint=(0.5, 1),
            halign='left',
            valign='middle'
        )
        self.status_label.bind(size=lambda *args: setattr(self.status_label, 'text_size', (self.status_label.width, self.status_label.height)))
        status_box.add_widget(self.status_label)

        content.add_widget(status_box)

        # Nästan inget mellanrum mellan status och meddelande
        content.add_widget(Widget(size_hint_y=0.01))  # Minimalt mellanrum

        # Meddelande
        message_box = BoxLayout(
            orientation='vertical',
            spacing=dp(0),
            size_hint=(1, 0.1)  # Minska höjden
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

        # Mellanrum före grafen
        content.add_widget(Widget(size_hint_y=0.03))  # Mellanrum

        # Plats för temperaturgrafen
        graph_container = BoxLayout(
            size_hint=(1, 0.49),  # Ge grafen mer utrymme
            padding=[0, dp(3), 0, 0]  # Lite padding överst
        )

        # Skapa graf-komponenten
        self.temperature_graph = TemperatureGraph()

        # Ställ in intervall för grafuppdatering (var 10:e sekund)
        Clock.schedule_interval(self.update_graph, 10)
        graph_container.add_widget(self.temperature_graph)

        content.add_widget(graph_container)
        
        # Lägg till innehållet till huvudlayout
        main_layout.add_widget(content)
        
        # Skapa action bar längst ner med knapparna
        action_bar = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.08),
            spacing=dp(10),
            padding=[0, dp(5), 0, 0]  # Padding överst
        )
        
        # Tillbakaknapp
        back_button = Button(
            text="Tillbaka",
            size_hint=(0.5, 1),
            background_normal='',
            background_color=(0.3, 0.4, 0.5, 1)
        )
        back_button.bind(on_release=self.go_back)
        action_bar.add_widget(back_button)
        
        # Inställningsknapp för framtida funktionalitet
        settings_button = Button(
            text="Inställningar",
            size_hint=(0.5, 1),
            background_normal='',
            background_color=(0.5, 0.5, 0.5, 1)  # Grå för att indikera inaktiv funktion
        )
        settings_button.bind(on_release=self.show_settings_info)
        action_bar.add_widget(settings_button)
        
        # Lägg till action bar längst ner
        main_layout.add_widget(action_bar)
        
        # Lägg till huvudlayout till skärmen
        self.add_widget(main_layout)
    
    def set_sensor(self, name, temp):
        """
        Sätt aktuell sensor och dess data
        """
        self.sensor_name = name
        self.temperature = temp

        # Uppdatera databasen med den nya temperaturen
        TemperatureHistory.add_temperature(name, temp)
        
        # Hämta sensorkonfiguration
        from models.sensor_config import SensorConfigs
        self.sensor_config = SensorConfigs.get_sensor_by_name(name)
        
        # Uppdatera UI-elementen
        self.title_label.text = f"{name}"  # Förenkla titeln
        self.temp_label.text = f"{temp:.1f}°C"
        
        # Sätt status och färg
        status = self.sensor_config.get_status(temp)
        status_color = self.sensor_config.get_status_color(temp)
        status_message = self.sensor_config.get_status_message(temp)
        
        # Uppdatera status-relaterade UI-element
        self.status_label.text = status.upper()
        self.status_label.color = status_color

        # Uppdatera grafen
        self.temperature_graph.set_sensor(name)
        self.temperature_graph.set_status_color(status_color)
        
        # Sätt samma färg på temperaturvisningen
        self.temp_label.color = status_color
        
        self.message_label.text = status_message
        
        # Uppdatera optimal range
        self.optimal_label.text = f"{self.sensor_config.optimal_range[0]}-{self.sensor_config.optimal_range[1]}°C"
    
    def go_back(self, instance):
        """
        Navigera tillbaka till huvudskärmen
        """
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'
    
    def show_settings_info(self, instance):
        """
        Visar information om kommande inställningsfunktionalitet
        """
        # Här kan du lägga till en toast eller popup som förklarar
        # att denna funktion kommer i framtida versioner
        print("Inställningsfunktionalitet kommer i framtida version")
        
        # Om du har en notifikations-toast kan du använda den:
        from notifications.notification_service import Notification
        from notifications.notification_manager import NotificationManager
        
        notification = Notification(
            "Inställningsfunktionalitet kommer i framtida version",
            Notification.INFO
        )
        
        NotificationManager.get_instance().show_notification(notification)

    def update_graph(self, dt):
        """Periodisk uppdatering av grafen"""
        if hasattr(self, 'temperature_graph') and self.sensor_name:
            self.temperature_graph.update()