"""
NotificationToast visar en tillfällig notifikation i UI.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.properties import NumericProperty, ObjectProperty

class NotificationToast(BoxLayout):
    """
    En toast-notifikation som visas tillfälligt och animeras in/ut.
    """
    
    # Egenskaper för animation
    x_offset = NumericProperty(0)
    notification = ObjectProperty(None)
    
    def __init__(self, notification, **kwargs):
        super(NotificationToast, self).__init__(**kwargs)
        
        # Spara notifikationen
        self.notification = notification
        
        # Grundinställningar för layout
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.width = dp(300)
        self.height = dp(100)
        self.padding = dp(15)
        self.spacing = dp(5)
        
        # Positionera utanför skärmen till att börja med (för animation in)
        self.x_offset = self.width
        self.pos_hint = {'top': 0.95, 'right': 1}
        
        # Skapa och lägg till innehåll
        self._setup_ui()
        
        # Starta animeringen
        self._animate_in()
    
    def _setup_ui(self):
        """Skapar UI-elementen för notifikationen"""
        # Tid och sensornamn
        header_box = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.3),
            spacing=dp(10)
        )
        
        # Visa tid
        time_label = Label(
            text=self.notification.get_formatted_time(),
            font_size=dp(12),
            size_hint=(0.3, 1),
            halign='left',
            valign='middle'
        )
        time_label.bind(size=lambda *args: setattr(time_label, 'text_size', (time_label.width, time_label.height)))
        header_box.add_widget(time_label)
        
        # Visa sensor om tillgänglig
        if self.notification.sensor_name:
            sensor_label = Label(
                text=self.notification.sensor_name,
                font_size=dp(14),
                bold=True,
                size_hint=(0.7, 1),
                halign='right',
                valign='middle'
            )
            sensor_label.bind(size=lambda *args: setattr(sensor_label, 'text_size', (sensor_label.width, sensor_label.height)))
            header_box.add_widget(sensor_label)
        
        self.add_widget(header_box)
        
        # Visa meddelande
        message_label = Label(
            text=self.notification.message,
            font_size=dp(14),
            size_hint=(1, 0.7),
            halign='left',
            valign='top'
        )
        message_label.bind(size=lambda *args: setattr(message_label, 'text_size', (message_label.width, None)))
        self.add_widget(message_label)
        
        # Rita bakgrund med korrekt färg
        with self.canvas.before:
            color = self.notification.get_color()
            Color(*color)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
            
            # För mörk kant
            Color(color[0]*0.8, color[1]*0.8, color[2]*0.8, color[3])
            self.border = RoundedRectangle(
                pos=self.pos, 
                size=self.size, 
                radius=[dp(10)],
                # 1dp kant
                source=''  # Tom källa för att bara få färg
            )
        
        # Uppdatera bakgrunden när vår position ändras
        self.bind(pos=self._update_rect, size=self._update_rect)
    
    def _update_rect(self, *args):
        """Uppdaterar bakgrundens position och storlek"""
        if hasattr(self, 'bg'):
            self.bg.pos = self.pos
            self.bg.size = self.size
        if hasattr(self, 'border'):
            self.border.pos = self.pos
            self.border.size = self.size
    
    def _animate_in(self):
        """Animerar in notifikationen från höger"""
        # Animera x_offset till 0 (flyttar den in på skärmen)
        anim = Animation(x_offset=0, duration=0.3)
        anim.start(self)
    
    def dismiss(self):
        """Animerar ut notifikationen och tar bort den"""
        # Animera x_offset till width (flyttar den ur skärmen)
        anim = Animation(x_offset=self.width, duration=0.3)
        anim.bind(on_complete=lambda *args: self._remove_self())
        anim.start(self)
    
    def _remove_self(self):
        """Tar bort notifikationen från dess förälder"""
        if self.parent:
            self.parent.remove_widget(self)
    
    def on_x_offset(self, instance, value):
        """Callback när x_offset ändras, uppdaterar position"""
        self.pos_hint = {'top': 0.95, 'right': 1 - value / self.width}