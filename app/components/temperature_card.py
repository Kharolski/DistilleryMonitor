from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior

class TemperatureCard(ButtonBehavior, BoxLayout):
    """
    Komponent som visar temperaturinformation för en sensor.
    Fungerar nu även som en knapp som kan klickas.
    """
    def __init__(self, name, temp, optimal_range, **kwargs):
        super(TemperatureCard, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(15)
        self.spacing = dp(10)
        self.size_hint = (1, None)
        self.height = dp(200)
        
        # Spara sensordata
        self.name = name
        self.temp = temp
        self.optimal_min, self.optimal_max = optimal_range
        
        # Bestäm kortets färg baserat på om temperaturen är inom optimalt intervall
        if self.optimal_min <= temp <= self.optimal_max:
            self.card_color = (0.2, 0.7, 0.2, 1)  # Grön
        elif self.optimal_min - 5 <= temp <= self.optimal_max + 5:
            self.card_color = (0.9, 0.7, 0.1, 1)  # Gul
        else:
            self.card_color = (0.8, 0.2, 0.2, 1)  # Röd
        
        # Skapa och lägg till widgets
        self._create_widgets()
        self._draw_background()
        
    def _create_widgets(self):
        # Sensornamn
        name_label = Label(
            text=self.name,
            font_size=dp(24),
            size_hint=(1, 0.3),
            bold=True
        )
        self.add_widget(name_label)
        
        # Temperaturvärde
        temp_label = Label(
            text=f"{self.temp:.1f}°C",
            font_size=dp(36),
            size_hint=(1, 0.4),
            bold=True
        )
        self.add_widget(temp_label)
        
        # Optimalt intervall
        optimal_label = Label(
            text=f"Optimal: {self.optimal_min}-{self.optimal_max}°C",
            font_size=dp(18),
            size_hint=(1, 0.3)
        )
        self.add_widget(optimal_label)
    
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
    

