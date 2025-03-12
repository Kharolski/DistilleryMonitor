"""
NotificationManager ansvarar för att visa notifikationer i UI.
"""

from kivy.clock import Clock
from .notification_service import NotificationService
from services.platform_notifier import PlatformNotifier
from services.sound_manager import SoundManager

class NotificationManager:
    """
    Hanterar visning av notifikationer i UI.
    Denna klass är ansvarig för att:
    - Ta emot notifikationer från NotificationService
    - Skapa och visa notifikations-toasts
    - Hantera notifikationshistorik i UI
    """
    
    # Singleton-instans
    _instance = None
    
    @staticmethod
    def get_instance():
        """Returnerar singleton-instansen"""
        if NotificationManager._instance is None:
            NotificationManager._instance = NotificationManager()
        return NotificationManager._instance
    
    def __init__(self):
        """Initierar notifikationshanteraren"""
        if NotificationManager._instance is not None:
            raise RuntimeError("Försök att instansiera en ny NotificationManager. Använd get_instance() istället.")
        
        # Få åtkomst till notifikationsservicen
        self.notification_service = NotificationService.get_instance()

        # Få åtkomst till plattformsnotifieraren
        self.platform_notifier = PlatformNotifier.get_instance()
        # Få åtkomst till ljudhanteraren
        self.sound_manager = SoundManager.get_instance()
        
        # Registrera callbackfunktionen hos servicen
        self.notification_service.set_notification_callback(self.show_notification)
        
        # Referens till huvudappen/root för att hantera toast-notifikationer
        self.app_root = None
        
        # Aktiv toast-notifikation
        self.active_toast = None
    
    def set_app_root(self, app_root):
        """
        Sätter referensen till appens root widget.
        
        Parametrar:
            app_root (Widget): Appens root widget där toasts ska läggas till
        """
        self.app_root = app_root
    
    def show_notification(self, notification):
        """
        Visar en notifikation som en toast och spelar ett ljud.
        
        Parametrar:
            notification (Notification): Notifikationen att visa
        """
        # Importera här för att undvika cykliska importer
        from components.notification_toast import NotificationToast
        from kivy.clock import Clock
        
        # Spela lämpligt ljud för notifikationstypen
        notification_type = notification.get_type_name().lower()
        self.sound_manager.play_sound(notification_type)
        
        # Om vi inte har en app_root, kan vi inte visa toasts
        if not self.app_root:
            print(f"Notifikation (ingen UI): {notification.message}")
            return
        
        # Använd Clock för att köra UI-uppdateringar på huvudtråden
        def _show_toast(dt):
            # Ta bort befintlig toast om den finns
            if self.active_toast:
                self.app_root.remove_widget(self.active_toast)
            
            # Skapa en ny toast
            toast = NotificationToast(notification)
            
            # Spara referens till aktiv toast
            self.active_toast = toast
            
            # Lägg till toasten till app_root
            self.app_root.add_widget(toast)
            
            # Schemalägg borttagning av toast efter 5 sekunder
            Clock.schedule_once(lambda dt: self._remove_toast(toast), 7)
        
        # Schemalägg att köra på huvudtråden
        Clock.schedule_once(_show_toast, 0)
    
    def show_system_notification(self, notification):
        """
        Visar en systemnotifikation som syns även när appen är minimerad.
        
        Parametrar:
            notification (Notification): Notifikationen att visa
        """
        # Bestäm viktighet baserat på notifikationstyp
        importance = "default"
        if notification.type == notification.WARNING:
            importance = "high"
        elif notification.type == notification.CRITICAL:
            importance = "critical"
        
        # Skapa en titel baserat på sensornamn
        title = notification.sensor_name or "Destillationsövervakare"
        
        # Visa systemnotifikation
        self.platform_notifier.show_notification(
            title, 
            notification.message, 
            importance
        )

    def _remove_toast(self, toast):
        """
        Tar bort en toast från UI.
        
        Parametrar:
            toast (NotificationToast): Toasten att ta bort
        """
        if toast.parent:
            toast.parent.remove_widget(toast)
        
        # Rensa referensen om det är den aktiva toasten
        if self.active_toast == toast:
            self.active_toast = None
    
    def process_sensor_update(self, name, temp):
        """
        Behandlar en sensoruppdatering och genererar notifikationer om nödvändigt.
        
        Parametrar:
            name (str): Sensorns namn
            temp (float): Aktuell temperatur
        """
        # Anropa notification service för att bearbeta data
        notification = self.notification_service.process_sensor_data(name, temp)
        
        # Om vi fick en notifikation som är WARNING eller CRITICAL,
        # visa den även som systemnotifikation
        if notification and notification.type in [notification.SUCCESS, notification.WARNING, notification.CRITICAL]:
            self.show_system_notification(notification)
    
    def get_notification_history(self):
        """Returnerar notifikationshistoriken"""
        return self.notification_service.get_notification_history()