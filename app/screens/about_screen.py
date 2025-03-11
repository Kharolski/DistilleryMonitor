from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp

class AboutScreen(Screen):
    """
    Skärm som visar information om appen och utvecklaren.
    """
    def __init__(self, **kwargs):
        super(AboutScreen, self).__init__(**kwargs)
        
        # Huvudlayout
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # Titel
        title = Label(
            text='Om Destillationsmonitorn',
            font_size=dp(26),
            size_hint=(1, 0.15),
            bold=True
        )
        self.layout.add_widget(title)
        
        # Informationstext
        info_text = """
Destillationsmonitor v1.0

Denna app övervakar temperaturen i olika delar av en destillationsprocess. 
Den visar realtidsinformation och historik för att hjälpa operatören att 
hålla optimala temperaturer.

Utvecklad av: Aleh Kharolski
Kontakt: kharolski@gmail.com
        """
        
        info_label = Label(
            text=info_text,
            font_size=dp(18),
            size_hint=(1, 0.75),
            halign='left',
            valign='top',
            text_size=(None, None)  # Anpassas i on_size
        )
        
        # Uppdatera textens storlek när skärmen ändrar storlek
        def update_text_size(instance, value):
            info_label.text_size = (value[0] - dp(40), None)
        
        self.bind(size=update_text_size)
        
        self.layout.add_widget(info_label)
        
        # Tillbaka-knapp
        back_button = Button(
            text='Tillbaka',
            size_hint=(1, 0.1),
            background_color=(0.3, 0.3, 0.3, 1)
        )
        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(back_button)
        
        self.add_widget(self.layout)
    
    def go_back(self, instance):
        """Gå tillbaka till hemskärmen"""
        # Sätt animationsriktning till höger
        self.manager.transition.direction = 'right'
        
        # Gå tillbaka till hemskärmen
        self.manager.current = 'home'