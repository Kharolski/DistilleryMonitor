from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder


# Omdefiniera hamburgerikonen utan padding
Builder.load_string('''
<IconButton>:
    size_hint: None, None
    size: dp(50), dp(50)
    pos_hint: {'center_y': 0.5}
    background_color: 0, 0, 0, 0
    padding: 0, 0, 0, 0  # Ta bort all padding runt knappen
    
    canvas.before:
        Color:
            rgba: 0.3, 0.6, 0.9, 1
        Rectangle:
            pos: self.pos
            size: self.size
    
    # Hamburgerikon med tre streck
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.x + dp(8), self.y + self.height * 0.7
            size: self.width - dp(16), dp(2)
        Rectangle:
            pos: self.x + dp(8), self.y + self.height * 0.5
            size: self.width - dp(16), dp(2)
        Rectangle:
            pos: self.x + dp(8), self.y + self.height * 0.3
            size: self.width - dp(16), dp(2)
''')


class IconButton(Button):
    """Knapp med hamburgerikon utan spacing"""
    pass


class DropDownMenu(BoxLayout):
    """
    En dropdown-meny som kan användas i applikationens övre del.
    """
    
    screen_manager = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(DropDownMenu, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (1, None)
        self.height = dp(50)
        self.padding = [0, 0, dp(10), 0]  # Ta bort vänster padding, behåll höger padding
        
        # Bakgrundsfärg för hela menyraden
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)  # Mörkgrå bakgrund
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            
        # Uppdatera bakgrundens position när widgeten flyttas
        self.bind(pos=self._update_rect, size=self._update_rect)
        
        # Skapa menyknappen med hamburgerikon
        self.menu_button = IconButton()
        
        # Skapa dropdown med tydliga breddegenskaper
        self.dropdown = DropDown()
        # VIKTIGT: Stäng av auto_width för att tvinga manuell bredd
        self.dropdown.auto_width = False
        # Sätt fast bredd för dropdown
        self.dropdown.width = dp(200)
        
        # Skapa menyalternativ med fast bredd
        btn = Button(
            text="Om appen",
            size_hint_y=None, 
            height=dp(50),
            size_hint_x=None,  # Måste ha None för att respektera width
            width=dp(200),
            background_normal='',
            background_color=(0.25, 0.25, 0.25, 1),
            color=(1, 1, 1, 1)
        )
        
        # Viktigt: Konfigurera texten korrekt
        btn.halign = 'left'
        btn.valign = 'middle'
        # Använd padding istället för padding_x (som är deprecated)
        btn.padding = [dp(10), 0, 0, 0]  # [left, top, right, bottom]
        # Sätt text_size för att texten ska flöda inom knappen
        btn.text_size = (dp(180), dp(50))
        
        # Bind menyval
        btn.bind(on_release=lambda btn: self.on_dropdown_select(self.show_about_screen))
        
        # Lägg till knappen till dropdown
        self.dropdown.add_widget(btn)
        
        # Bind dropdown till menyknappen
        self.menu_button.bind(on_release=self.dropdown.open)
        
        # Lägg till menyknappen till layouten (utan extra spacing)
        self.add_widget(self.menu_button)
        
        # App-titel för att använda utrymmet bredvid menyknappen
        self.app_title = Label(
            text="Destillering",
            size_hint=(1, 1),
            color=(1, 1, 1, 1),  # Vit text
            font_size=dp(18),
            bold=True
        )
        
        # Centrera texten
        self.app_title.bind(size=self._update_title_pos)
        
        self.add_widget(self.app_title)
    
    def on_dropdown_select(self, callback):
        """Hantera val i dropdown-menyn"""
        self.dropdown.dismiss()
        callback()
    
    def _update_title_pos(self, instance, value):
        """Uppdatera titelns position för centrering"""
        instance.text_size = value
        instance.halign = 'center'
        instance.valign = 'middle'
    
    def _update_rect(self, *args):
        """Uppdatera bakgrundsfärgen när widgeten flyttas eller ändrar storlek"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def show_about_screen(self):
        """Visa Om appen-skärmen"""
        if self.screen_manager:
            self.screen_manager.transition.direction = 'left'
            self.screen_manager.current = 'about'