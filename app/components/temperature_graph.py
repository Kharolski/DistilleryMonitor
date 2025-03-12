"""
Grafkomponent för att visa temperaturhistorik
"""

from kivy_garden.graph import Graph, MeshLinePlot
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from datetime import datetime
from data.temperature_history import TemperatureHistory

class TemperatureGraph(BoxLayout):
    """
    Återanvändbar komponent för att visa temperaturhistorik som en graf
    """
    
    def __init__(self, **kwargs):
        super(TemperatureGraph, self).__init__(orientation='vertical', 
                                               spacing=dp(5), 
                                               **kwargs)
        
        # Sensorn som visas
        self.sensor_name = None
        
        # Status-färg för linjen
        self.status_color = [0, 1, 0, 1]  # Standard: grön
        
        # Skapa graf-widget
        self.graph = Graph(
            xlabel='Tid',
            ylabel='°C',
            x_ticks_minor=0,
            x_ticks_major=5,
            y_ticks_major=2,
            y_grid_label=True,
            x_grid_label=True,
            padding=dp(5),
            x_grid=True,
            y_grid=True,
            xmin=0,
            xmax=19,  # För 20 punkter (0-19)
            ymin=70,
            ymax=90,
            size_hint=(1, 0.85)
        )
        
        # Skapa linjeplotten
        self.plot = MeshLinePlot(color=self.status_color)
        self.graph.add_plot(self.plot)
        
        # Lägg till grafen till layouten
        self.add_widget(self.graph)
        
        # Skapa statistik-label
        self.stats_label = Label(
            text="Statistik:  Min: --  Max: --  Medel: --",
            font_size=dp(14),
            size_hint=(1, 0.15),
            halign='center'
        )
        self.stats_label.bind(size=lambda *args: setattr(self.stats_label, 'text_size', (self.stats_label.width, None)))
        
        # Lägg till statistik-labeln
        self.add_widget(self.stats_label)
    
    def set_sensor(self, sensor_name):
        """
        Sätt sensorn som grafen ska visa och uppdatera data
        
        Args:
            sensor_name (str): Namnet på sensorn
        """
        self.sensor_name = sensor_name
        self.update()
    
    def set_status_color(self, color):
        """
        Uppdatera färgen på grafen baserat på aktuell status
        
        Args:
            color (list): RGBA-färg [r, g, b, a]
        """
        self.status_color = color
        if self.plot:
            self.plot.color = self.status_color
    
    def update(self):
        """
        Uppdatera grafen med senaste data från databasen
        """
        if not self.sensor_name:
            return
        
        # Hämta temperaturhistorik från databasen
        history = TemperatureHistory.get_history(self.sensor_name, limit=20)
        
        if not history:
            # Om ingen historik finns, visa tomt
            self.plot.points = []
            self.stats_label.text = "Statistik:  Min: --  Max: --  Medel: --"
            return
        
        # Extrahera temperatur och tidsstämplar
        temperatures = [entry[0] for entry in history]
        timestamps = [entry[1] for entry in history]
        
        # Konvertera tidsstämplar till läsbara tider (HH:MM)
        formatted_times = []
        for ts in timestamps:
            try:
                dt = datetime.fromisoformat(ts)
                formatted_times.append(dt.strftime("%H:%M"))
            except (ValueError, TypeError):
                formatted_times.append("--:--")
        
        # Sätt datapunkter för grafen
        self.plot.points = [(i, temperatures[i]) for i in range(len(temperatures))]
        
        # Justera y-axelns gränser baserat på data
        if temperatures:
            min_temp = min(temperatures) - 1
            max_temp = max(temperatures) + 1
            
            self.graph.ymin = min_temp
            self.graph.ymax = max_temp
        
        # Uppdatera x-axelns etiketter (visa bara var 5:e)
        x_labels = {i: formatted_times[i] for i in range(0, len(formatted_times), 5)}
        self.graph.x_ticks_major_labels = x_labels
        
        # Uppdatera statistiklabeln
        stats = TemperatureHistory.get_statistics(self.sensor_name)
        self.stats_label.text = f"Statistik:  Min: {stats['min_temp']:.1f}°C  Max: {stats['max_temp']:.1f}°C  Medel: {stats['avg_temp']:.1f}°C"