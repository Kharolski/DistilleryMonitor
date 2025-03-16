from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle

class AboutScreen(MDScreen):
    """
    Skärm som visar information om appen och utvecklaren.
    """
    def __init__(self, **kwargs):
        super(AboutScreen, self).__init__(**kwargs)
        
        # Huvudlayout
        self.layout = MDBoxLayout(
            orientation='vertical', 
            padding=dp(20), 
            spacing=dp(20),
            md_bg_color=[0.12, 0.12, 0.12, 1]  # Svart bakgrund
        )
        
        # Titel
        title = MDLabel(
            text='Om Destillationsmonitorn',
            font_style='Headline',  # Material Design typografi
            size_hint=(1, 0.15),
            halign='center',
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1]  # Vit text för kontrast mot svart bakgrund
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
        
        info_label = MDLabel(
            text=info_text,
            font_style='Body',  # Material Design typografi
            size_hint=(1, 0.75),
            halign='left',
            valign='top',
            text_size=(None, None),  # Anpassas i on_size
            theme_text_color="Custom",
            text_color=[0.9, 0.9, 0.9, 1]  # Ljusgrå text för bättre läsbarhet
        )
        
        # Uppdatera textens storlek när skärmen ändrar storlek
        def update_text_size(instance, value):
            info_label.text_size = (value[0] - dp(40), None)
        
        self.bind(size=update_text_size)
        
        self.layout.add_widget(info_label)
        
        # Tillbaka-knapp - uppdaterad för KivyMD 2.0.1
        back_button = MDButton(
            MDButtonText(
                text='Tillbaka',
                theme_text_color="Custom",
                text_color=[1, 1, 1, 1]  # Vit text
            ),
            style="filled",  # Lägg till stil
            size_hint=(1, 0.1),
            md_bg_color=[0.2, 0.2, 0.2, 1],  # Mörkgrå knapp
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
