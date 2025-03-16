from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.clock import Clock

class DropDownMenu(MDBoxLayout):
    """
    En dropdown-meny som kan användas i applikationens övre del.
    Implementerad med KivyMD-komponenter.
    """
    
    screen_manager = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(DropDownMenu, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (1, None)
        self.height = dp(50)  # Material Design standard höjd
        self.md_bg_color = [0.12, 0.12, 0.12, 1]  # Mörkgrå bakgrund
        
        # Skapa menyknappen med hamburgerikon - nu med vit färg
        self.menu_button = MDIconButton(
            icon="menu",
            pos_hint={"center_y": 0.5},
            theme_icon_color="Custom",
            icon_color=[1, 1, 1, 1],  # Vit ikon
            style="standard"  # Lägg till stil (kan vara "standard", "filled", "outlined", "tonal")
        )
        
        # Skapa dropdown-meny med KivyMD - ändra viewclass till "MDListItem"
        menu_items = [
            {
                "text": "Om appen",
                "height": dp(50),
                "on_release": lambda x=0: self.on_dropdown_select(self.show_about_screen),
                "text_color": [1, 1, 1, 1],  # Vit text
                "md_bg_color": [0.2, 0.2, 0.2, 1],  # Bakgrundsfärg för detta element
            },
            {
                "text": "Inställningar",
                "height": dp(50),
                "on_release": lambda x=0: self.on_dropdown_select(self.show_settings),
                "text_color": [1, 1, 1, 1],
                "md_bg_color": [0.2, 0.2, 0.2, 1],  # Bakgrundsfärg för detta element
            },
            {
                "text": "Hjälp",
                "height": dp(50),
                "on_release": lambda x=0: self.on_dropdown_select(self.show_help),
                "text_color": [1, 1, 1, 1],
                "md_bg_color": [0.2, 0.2, 0.2, 1],  # Bakgrundsfärg för detta element
            }
        ]
        
        # Använd moderna egenskaper för menyn
        self.dropdown = MDDropdownMenu(
            caller=self.menu_button,
            items=menu_items,
            width=dp(200),  # Fast bredd
            elevation=4,
            radius=[dp(10), dp(10), dp(10), dp(10)],  # Rundade hörn
        )
        
        # Bind dropdown till menyknappen
        self.menu_button.bind(on_release=self.open_dropdown)
        
        # Lägg till menyknappen till layouten
        self.add_widget(self.menu_button)
        
        # App-titel för att använda utrymmet bredvid menyknappen
        self.app_title = MDLabel(
            text="Destillering",
            halign="center",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],  # Vit text
            # Ändra från "Title" till "Body" eftersom font_style har ändrats i KivyMD 2.0.1
            bold=True
        )
        
        self.add_widget(self.app_title)
    
    def open_dropdown(self, instance):
        """Öppna dropdown-menyn"""
        self.dropdown.open()
    
    def on_dropdown_select(self, callback):
        """Hantera val i dropdown-menyn"""
        self.dropdown.dismiss()
        # Använd Clock för att undvika problem med samtidig stängning och navigering
        Clock.schedule_once(lambda dt: callback(), 0.1)
    
    def show_about_screen(self):
        """Visa Om appen-skärmen"""
        if self.screen_manager:
            self.screen_manager.transition.direction = 'left'
            self.screen_manager.current = 'about'