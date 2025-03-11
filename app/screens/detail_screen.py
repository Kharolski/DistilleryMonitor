from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy_garden.graph import Graph, MeshLinePlot
from kivy.clock import Clock
import random
from datetime import datetime, timedelta

class DetailScreen(Screen):
    """
    Detaljskärm som visar temperaturhistorik för en sensor.
    """
    def __init__(self, **kwargs):
        super(DetailScreen, self).__init__(**kwargs)
        
        # Huvudlayout
        self.layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        # Sensor-information
        self.sensor_info = BoxLayout(orientation='vertical', size_hint=(1, 0.2))
        self.sensor_name = Label(text="Sensor", font_size=dp(28), bold=True, size_hint=(1, 0.5))
        self.current_temp = Label(text="Temperatur: 0.0°C", font_size=dp(22), size_hint=(1, 0.5))
        self.sensor_info.add_widget(self.sensor_name)
        self.sensor_info.add_widget(self.current_temp)
        
        # Graf för temperaturhistorik
        self.graph_container = BoxLayout(orientation='vertical', size_hint=(1, 0.6))
        self.graph = Graph(
            xlabel='Tid', 
            ylabel='Temp (°C)',
            x_ticks_minor=5,
            x_ticks_major=10,
            y_ticks_major=5,
            y_grid_label=True,
            x_grid_label=True,
            padding=dp(5),
            x_grid=True,
            y_grid=True,
            xmin=0,
            xmax=60,  # Visa 60 minuter
            ymin=0,
            ymax=100  # Max temperatur 100°C
        )
        self.graph_container.add_widget(self.graph)
        
        # Statistik
        self.stats_container = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        self.min_temp = Label(text="Min: 0.0°C")
        self.max_temp = Label(text="Max: 0.0°C")
        self.avg_temp = Label(text="Medel: 0.0°C")
        
        self.stats_container.add_widget(self.min_temp)
        self.stats_container.add_widget(self.max_temp)
        self.stats_container.add_widget(self.avg_temp)
        
        # Knappar
        self.buttons_container = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=dp(10))
        self.back_button = Button(
            text="Tillbaka", 
            background_color=(0.3, 0.3, 0.3, 1),
            size_hint=(0.5, 1)
        )
        self.back_button.bind(on_press=self.go_back)
        
        self.refresh_button = Button(
            text="Uppdatera", 
            background_color=(0.3, 0.5, 0.9, 1),
            size_hint=(0.5, 1)
        )
        self.refresh_button.bind(on_press=self.refresh_graph)
        
        self.buttons_container.add_widget(self.back_button)
        self.buttons_container.add_widget(self.refresh_button)
        
        # Lägg till alla containers till huvudlayouten
        self.layout.add_widget(self.sensor_info)
        self.layout.add_widget(self.graph_container)
        self.layout.add_widget(self.stats_container)
        self.layout.add_widget(self.buttons_container)
        
        self.add_widget(self.layout)
        
        # Data för grafen
        self.plot = None
        self.sensor_data = {}
        self.temp_history = []
        
        # Initialisera plotten direkt
        self.plot = MeshLinePlot(color=[0, 1, 0, 1])
        self.graph.add_plot(self.plot)
    
    def set_sensor(self, name, temp, optimal_range):
        """Sätt aktuell sensor och dess data"""
        self.sensor_name.text = name
        self.current_temp.text = f"Temperatur: {temp:.1f}°C"
        
        # Spara sensordata
        self.sensor_data = {
            'name': name,
            'temp': temp,
            'optimal_min': optimal_range[0],
            'optimal_max': optimal_range[1]
        }
        
        # Anpassa grafens y-axel baserat på optimalt intervall
        buffer = 20  # Lägg till lite marginal
        self.graph.ymin = max(0, optimal_range[0] - buffer)
        self.graph.ymax = optimal_range[1] + buffer
        
        # Generera mock-historik för demonstrationsändamål
        self.generate_mock_history()
        
        # Uppdatera grafen
        if self.plot:
            self.update_graph()
    
    def generate_mock_history(self):
        """Generera simulerad temperaturhistorik"""
        self.temp_history = []
        base_temp = self.sensor_data['temp']
        optimal_min = self.sensor_data['optimal_min']
        optimal_max = self.sensor_data['optimal_max']
        
        # Generera 60 datapunkter (en per minut för senaste timmen)
        for i in range(60):
            # Simulera temperatur runt bastemperaturen
            variation = random.uniform(-5, 5)
            temp = base_temp + variation
            
            # Lägg till tidpunkt och temperatur
            now = datetime.now() - timedelta(minutes=60-i)
            self.temp_history.append({
                'timestamp': now,
                'temp': temp
            })
        
        # Beräkna statistik
        temps = [entry['temp'] for entry in self.temp_history]
        self.min_temp.text = f"Min: {min(temps):.1f}°C"
        self.max_temp.text = f"Max: {max(temps):.1f}°C"
        self.avg_temp.text = f"Medel: {sum(temps)/len(temps):.1f}°C"
    
    def update_graph(self):
        """Uppdatera grafen med historikdata"""
        if not self.temp_history:
            return
        
        try:
            # Skapa datapunkter för grafen
            points = [(i, entry['temp']) for i, entry in enumerate(self.temp_history)]
            self.plot.points = points
        except Exception as e:
            # Behåll en enkel felhantering för att fånga allvarliga problem
            print(f"Error updating graph: {e}")
    
    def refresh_graph(self, instance):
        """Uppdatera grafen med ny data (för testning)"""
        self.generate_mock_history()
        self.update_graph()
    
    def go_back(self, instance):
        """Gå tillbaka till hemskärmen"""
        # Sätt animationsriktning till höger
        self.manager.transition.direction = 'right'
        
        # Gå tillbaka till hemskärmen
        self.manager.current = 'home'