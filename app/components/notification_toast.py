"""
NotificationToast visar en tillfällig notifikation i UI med KivyMD-komponenter.
"""

from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.animation import Animation
from kivy.properties import NumericProperty, ObjectProperty
from kivy.metrics import dp


class NotificationToast(MDCard):
    """
    En toast-notifikation som visas tillfälligt och animeras in/ut.
    Implementerad med KivyMD-komponenter för ett modernt utseende.
    """
    
    # Egenskaper för animation
    x_offset = NumericProperty(0)
    notification = ObjectProperty(None)
    
    def __init__(self, notification, **kwargs):
        # Grundinställningar för MDCard
        kwargs['orientation'] = 'vertical'
        kwargs['size_hint'] = (None, None)
        kwargs['width'] = dp(300)
        kwargs['height'] = dp(100)
        kwargs['padding'] = dp(15)
        kwargs['elevation'] = 6
        kwargs['radius'] = [dp(10)]
        
        # Sätt bakgrundsfärg med theme_bg_color
        kwargs['theme_bg_color'] = "Custom"
        kwargs['md_bg_color'] = notification.get_color()
        
        # Anropa förälderns konstruktor med alla inställningar
        super(NotificationToast, self).__init__(**kwargs)
        
        # Spara notifikationen
        self.notification = notification
        
        # Positionera utanför skärmen till att börja med (för animation in)
        self.x_offset = self.width
        self.pos_hint = {'top': 0.95, 'right': 1}
        
        # Skapa och lägg till innehåll
        self._setup_ui()
        
        # Starta animeringen
        self._animate_in()
    
    def _setup_ui(self):
        """Skapar UI-elementen för notifikationen med KivyMD-komponenter"""
        # Tid och sensornamn
        header_box = MDBoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.3),
            spacing=dp(10)
        )
        
        # Visa tid - ändra font_style till font_size
        time_label = MDLabel(
            text=self.notification.get_formatted_time(),
            font_size=dp(12),
            size_hint=(0.3, 1),
            halign='left',
            valign='middle',
            theme_text_color="Custom",
            text_color=[0, 0, 0, 1]  # Svart text för bättre kontrast
        )
        time_label.bind(size=lambda *args: setattr(time_label, 'text_size', (time_label.width, time_label.height)))
        header_box.add_widget(time_label)
        
        # Visa sensor om tillgänglig
        if self.notification.sensor_name:
            sensor_label = MDLabel(
                text=self.notification.sensor_name,
                font_size=dp(16),
                bold=True,
                size_hint=(0.7, 1),
                halign='right',
                valign='middle',
                theme_text_color="Custom",
                text_color=[0, 0, 0, 1]  # Svart text för bättre kontrast
            )
            sensor_label.bind(size=lambda *args: setattr(sensor_label, 'text_size', (sensor_label.width, sensor_label.height)))
            header_box.add_widget(sensor_label)
        
        self.add_widget(header_box)
        
        # Visa meddelande
        message_label = MDLabel(
            text=self.notification.message,
            font_size=dp(14),
            size_hint=(1, 0.7),
            halign='left',
            valign='top',
            theme_text_color="Custom",
            text_color=[0, 0, 0, 1]  # Svart text för bättre kontrast
        )
        message_label.bind(size=lambda *args: setattr(message_label, 'text_size', (message_label.width, None)))
        self.add_widget(message_label)
    
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