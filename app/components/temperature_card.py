from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from models.sensor_config import SensorConfigs

class TemperatureCard(ButtonBehavior, BoxLayout):
    """
    Komponent som visar temperaturinformation för en sensor.
    Fungerar även som en knapp som kan klickas.
    """
    def __init__(self, name, temp, **kwargs):
        super(TemperatureCard, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(15)
        self.spacing = dp(10)
        self.size_hint = (1, None)
        self.height = dp(200)
        
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
        
        # Skapa och lägg till widgets
        self._create_widgets()
        self._draw_background()
        
    def _create_widgets(self):
        # Sensornamn
        name_label = Label(
            text=self.name,
            font_size=dp(24),
            size_hint=(1, 0.2),
            bold=True
        )
        self.add_widget(name_label)
        
        # Temperaturvärde
        temp_label = Label(
            text=f"{self.temp:.1f}°C",
            font_size=dp(36),
            size_hint=(1, 0.3),
            bold=True
        )
        self.add_widget(temp_label)
        
        # Optimalt intervall
        optimal_label = Label(
            text=f"Optimal: {self.sensor_config.optimal_range[0]}-{self.sensor_config.optimal_range[1]}°C",
            font_size=dp(16),
            size_hint=(1, 0.2)
        )
        self.add_widget(optimal_label)
        
        # Status meddelande
        status_label = Label(
            text=self.status_message,
            font_size=dp(14),
            size_hint=(1, 0.3),
            halign='center',
            valign='middle'
        )
        # Ställ in text_size för att text ska radbrytas
        status_label.bind(size=lambda *args: setattr(status_label, 'text_size', (status_label.width, None)))
        self.add_widget(status_label)
    
    def _draw_background(self):
        # Rita bakgrunden med avrundade hörn
        with self.canvas.before:
            Color(*self.card_color)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])
        
        # Uppdatera bakgrundens position när widgeten flyttas
        self.bind(pos=self._update_bg, size=self._update_bg)
    
    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
    
    def update_temperature(self, new_temp):
        """
        Uppdaterar temperaturvärdet och korsets utseende.
        """
        self.temp = new_temp
        self.card_color = self.sensor_config.get_status_color(new_temp)
        self.status = self.sensor_config.get_status(new_temp)
        self.status_message = self.sensor_config.get_status_message(new_temp)
        
        # Ta bort alla widgets
        self.clear_widgets()
        
        # Återskapa widgets med ny data
        self._create_widgets()
        
        # Uppdatera bakgrundsfärg
        with self.canvas.before:
            self.canvas.before.clear()
            Color(*self.card_color)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])