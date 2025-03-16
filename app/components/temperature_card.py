from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivy.metrics import dp
from models.sensor_config import SensorConfigs
from kivy.properties import ListProperty

class TemperatureCard(MDCard, RectangularRippleBehavior):
    """
    Komponent som visar temperaturinformation för en sensor.
    Fungerar även som en knapp som kan klickas med ripple-effekt.
    """
    
    def __init__(self, name, temp, **kwargs):
        # Spara sensordata
        self.name = name
        self.temp = temp
        
        # Hämta sensorkonfiguration från vår nya modell
        self.sensor_config = SensorConfigs.get_sensor_by_name(name)
        if not self.sensor_config:
            # Fallback om konfigurationen inte finns
            print(f"Warning: No sensor configuration found for {name}")
            optimal_range = kwargs.get('optimal_range', (0, 100))
            
            from models.sensor_config import SensorConfig
            self.sensor_config = SensorConfig(
                name=name,
                not_ready_range=(0, optimal_range[0]),
                optimal_range=optimal_range,
                warning_range=(optimal_range[1], optimal_range[1] + 5),
                critical_threshold=optimal_range[1] + 5
            )
        
        # Bestäm kortets färg baserat på sensorkonfigurationen
        self.card_color = self.sensor_config.get_status_color(temp)
        self.status = self.sensor_config.get_status(temp)
        self.status_message = self.sensor_config.get_status_message(temp)
        
        # Ställ in kortets egenskaper i kwargs
        kwargs['orientation'] = 'vertical'
        kwargs['padding'] = dp(15)
        kwargs['spacing'] = dp(10)
        kwargs['size_hint'] = (1, None)
        kwargs['height'] = dp(160)
        kwargs['radius'] = [dp(15)]
        kwargs['style'] = "elevated"
        kwargs['theme_bg_color'] = "Custom"
        kwargs['md_bg_color'] = self.card_color
        
        # Anropa förälderns konstruktor med alla inställningar
        super(TemperatureCard, self).__init__(**kwargs)
        
        # Skapa och lägg till widgets
        self._create_widgets()
    
    def _create_widgets(self):
        # Rensa eventuella tidigare widgets
        self.clear_widgets()
        
        # Sensornamn
        name_label = MDLabel(
            text=self.name,
            font_size=dp(18),
            size_hint=(1, 0.2),
            halign="left",
            bold=True,
            theme_text_color="Custom",
            text_color=[0, 0, 0, 1]  # Svart text
        )
        self.add_widget(name_label)
        
        # Temperaturvärde
        temp_label = MDLabel(
            text=f"{self.temp:.1f}°C",
            font_style="Headline",
            role="medium",
            size_hint=(1, 0.3),
            halign="center",
            theme_text_color="Custom",
            text_color=[0, 0, 0, 1]  # Svart text
        )
        self.add_widget(temp_label)
        
        # Optimalt intervall
        optimal_label = MDLabel(
            text=f"Optimal: {self.sensor_config.optimal_range[0]}-{self.sensor_config.optimal_range[1]}°C",
            font_size=dp(14),
            size_hint=(1, 0.2),
            halign="center",
            theme_text_color="Custom",
            text_color=[0, 0, 0, 1]  # Svart text
        )
        self.add_widget(optimal_label)
        
        # Status meddelande
        status_label = MDLabel(
            text=self.status_message,
            font_size=dp(14),
            size_hint=(1, 0.3),
            halign="center",
            valign="middle",
            theme_text_color="Custom",
            text_color=[0, 0, 0, 1]  # Svart text
        )
        self.add_widget(status_label)
    
    def update_temperature(self, new_temp):
        """
        Uppdaterar temperaturvärdet och kortets utseende.
        """
        self.temp = new_temp
        self.card_color = self.sensor_config.get_status_color(new_temp)
        self.status = self.sensor_config.get_status(new_temp)
        self.status_message = self.sensor_config.get_status_message(new_temp)
        
        # Uppdatera kortets bakgrundsfärg
        self.md_bg_color = self.card_color
        
        # Återskapa widgets med ny data
        self._create_widgets()