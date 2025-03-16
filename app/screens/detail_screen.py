from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText
from kivy.metrics import dp
from components.temperature_graph import TemperatureGraph
from data.temperature_history import TemperatureHistory
from kivy.clock import Clock
from kivymd.uix.card import MDCard
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivy.graphics import Color, Rectangle

class DetailScreen(MDScreen):
    """
    Skärm som visar detaljerad information om en temperaturgivare.
    """
    
    def __init__(self, **kwargs):
        super(DetailScreen, self).__init__(**kwargs)
        
        # Ställ in bakgrund för hela skärmen med canvas
        with self.canvas.before:
            Color(0.12, 0.12, 0.12, 1)  # Vit färg (RGBA)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        
        # Uppdatera rektangeln när skärmens storlek ändras
        self.bind(size=self._update_bg, pos=self._update_bg)
        
        # Initiera huvudvariabler
        self.sensor_name = ""
        self.temperature = 0.0
        self.sensor_config = None
        
        # Skapa huvudlayout
        main_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(15),  # Minska padding för mer kompakt layout
            spacing=dp(8),   # Minska spacing
            md_bg_color=[0, 0, 0, 0]  # bakgrund
        )
        
        # Titel för skärmen
        title_container = MDBoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.08),  # Minska höjden för en mer kompakt layout
            padding=[0, 0, 0, dp(5)],  # Lägg till lite padding i botten
            md_bg_color=[0, 0, 0, 0]  # Transparant bakgrund
        )
        
        self.title_label = MDLabel(
            text="Sensor Details",
            font_style="Title",  
            halign='center',
            size_hint=(1, 1),
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1]  # Vit text för kontrast mot svart bakgrund
        )
        
        title_container.add_widget(self.title_label)
        main_layout.add_widget(title_container)
        
        # Innehållslayout
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(-5),  # Ingen standardspacing - vi styr detta individuellt
            size_hint=(1, 0.84),
            md_bg_color=[0, 0, 0, 0]  # transparant bakgrund
        )

        # Skapa ett kort för sensorinformation
        info_card = MDCard(
            orientation="vertical",
            padding=dp(15),
            elevation=4,  # Lägg till skugga för kontrast mot svart bakgrund
            radius=[10, 10, 10, 10],  # Behåll rundade hörn
            size_hint=(1, None),
            height=dp(180),
            theme_bg_color="Custom",
            md_bg_color=[0.2, 0.2, 0.2, 1]  # Mörkgrå bakgrund för kortet
        )

        # Temperaturvisning
        temp_box = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint=(1, 0.1),  # Minska höjden
            md_bg_color=[0, 0, 0, 0]  # Transparant bakgrund
        )

        temp_header = MDLabel(
            text="Aktuell temperatur:",
            font_style="Label",
            size_hint=(0.5, 1),
            halign='right',
            valign='middle',
            theme_text_color="Custom",
            text_color=[0.9, 0.9, 0.9, 1]  # Ljusgrå text för bättre läsbarhet
        )
        temp_box.add_widget(temp_header)

        self.temp_label = MDLabel(
            text="--°C",
            font_style="Headline",
            bold=True,
            size_hint=(0.5, 1),
            halign='left',
            valign='middle',
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1]  # Vit text för temperatur
        )
        temp_box.add_widget(self.temp_label)

        info_card.add_widget(temp_box)

        # Optimal temperaturintervall - direkt under temperatur utan mellanrum
        optimal_box = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint=(1, 0.1),  # Minska höjden
            padding=[0, 0, 0, 0],  # Ingen padding
            md_bg_color=[0, 0, 0, 0]  # Mörkgrå bakgrund
        )

        optimal_header = MDLabel(
            text="Optimalt intervall:",
            font_style="Label",
            size_hint=(0.5, 1),
            halign='right',
            valign='middle',
            theme_text_color="Custom",
            text_color=[0.9, 0.9, 0.9, 1]  # Ljusgrå text
        )
        optimal_box.add_widget(optimal_header)

        self.optimal_label = MDLabel(
            text="--",
            font_style="Label",
            size_hint=(0.5, 1),
            halign='left',
            valign='middle',
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1]  # Vit text
        )
        optimal_box.add_widget(self.optimal_label)

        info_card.add_widget(optimal_box)

        # Lägg till mellanrum mellan temperatur och status
        info_card.add_widget(Widget(size_hint_y=0.03))  # Mellanrum

        # Status
        status_box = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint=(1, 0.1),  # Minska höjden
            md_bg_color=[0, 0, 0, 0]  # Transparant bakgrund
        )

        status_header = MDLabel(
            text="Status:",
            font_style="Label",
            size_hint=(0.5, 1),
            halign='right',
            valign='middle',
            theme_text_color="Custom",
            text_color=[0.9, 0.9, 0.9, 1]  # Ljusgrå text
        )
        status_box.add_widget(status_header)

        self.status_label = MDLabel(
            text="--",
            font_style="Title",
            bold=True,
            size_hint=(0.5, 1),
            halign='left',
            valign='middle',
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1]  # Vit text som standard, ändras dynamiskt
        )
        status_box.add_widget(self.status_label)

        info_card.add_widget(status_box)

        # Nästan inget mellanrum mellan status och meddelande
        info_card.add_widget(Widget(size_hint_y=0.01))  # Minimalt mellanrum

        # Meddelande
        message_box = MDBoxLayout(
            orientation='vertical',
            spacing=dp(0),
            size_hint=(1, 0.1),  # Minska höjden
            md_bg_color=[0, 0, 0, 0]  # Transparant bakgrund
        )

        self.message_label = MDLabel(
            text="Ingen information tillgänglig",
            font_style="Body",
            size_hint=(1, 1),
            halign='center',
            valign='middle',
            theme_text_color="Custom",
            text_color=[0.9, 0.9, 0.9, 1]  # Ljusgrå text
        )

        message_box.add_widget(self.message_label)
        info_card.add_widget(message_box)
        
        # Lägg till infokortet till innehållet
        content.add_widget(info_card)
        
        # Mellanrum före grafen
        content.add_widget(Widget(size_hint_y=0.03))  # Mellanrum

        # Plats för temperaturgrafen
        graph_card = MDCard(
            orientation="vertical",
            padding=dp(8),
            elevation=4,  # Lägg till skugga för kontrast
            radius=[10, 10, 10, 10],  # Behåll rundade hörn
            size_hint=(1, 0.49),  # Ge grafen mer utrymme
            theme_bg_color="Custom",
            md_bg_color=[0.2, 0.2, 0.2, 1]  # Mörkgrå bakgrund för grafen
        )

        # Skapa graf-komponenten
        self.temperature_graph = TemperatureGraph()

        # Ställ in intervall för grafuppdatering (var 5:e sekund)
        Clock.schedule_interval(self.update_graph, 5)
        graph_card.add_widget(self.temperature_graph)

        content.add_widget(graph_card)
        
        # Lägg till innehållet till huvudlayout
        main_layout.add_widget(content)
        
        # Skapa action bar längst ner med knapparna
        action_bar = MDBoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.07),
            spacing=dp(10),
            padding=[dp(10), dp(5), dp(10), dp(5)],  # Padding överst
            md_bg_color=[0, 0, 0, 0]  # Transparent  bakgrund
        )
        
        # Tillbakaknapp
        back_button = MDButton(
            MDButtonText(
                text="Tillbaka",
            ),
            style="filled",
            size_hint=(0.4, None),
            height=dp(40),
            theme_bg_color="Custom",
            md_bg_color=[0.2, 0.4, 0.6, 1]
        )
        back_button.bind(on_release=self.go_back)
        action_bar.add_widget(back_button)

        # Inställningsknapp för framtida funktionalitet
        settings_button = MDButton(
            MDButtonText(
                text="Inställningar",
            ),
            style="filled",
            size_hint=(0.6, None),
            height=dp(40),
            theme_bg_color="Custom",
            md_bg_color=[0.6, 0.4, 0.2, 1]
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
        self.status_label.text_color = status_color

        # Uppdatera grafen
        self.temperature_graph.set_sensor(name)
        self.temperature_graph.set_status_color(status_color)
        
        # Sätt samma färg på temperaturvisningen
        self.temp_label.text_color = status_color
        
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

    def _update_bg(self, *args):
        """Uppdaterar bakgrundsrektangelns storlek och position"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size