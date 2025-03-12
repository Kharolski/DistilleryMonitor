"""
PlatformNotifier hanterar systemnotifikationer på olika plattformar.
"""

import platform
import os
from kivy.clock import Clock

class PlatformNotifier:
    """
    Hanterar systemnotifikationer för olika plattformar (Android, iOS, Desktop).
    """
    
    # Singleton-instans
    _instance = None
    
    @staticmethod
    def get_instance():
        """Returnerar singleton-instansen"""
        if PlatformNotifier._instance is None:
            PlatformNotifier._instance = PlatformNotifier()
        return PlatformNotifier._instance
    
    def __init__(self):
        """Initierar plattformsnotifieraren"""
        if PlatformNotifier._instance is not None:
            raise RuntimeError("Försök att instansiera en ny PlatformNotifier. Använd get_instance() istället.")
        
        # Identifiera plattform
        self.platform = self._identify_platform()
        print(f"Plattformsnotifierare initierad för: {self.platform}")
    
    def _identify_platform(self):
        """Identifierar vilken plattform appen körs på"""
        system = platform.system()
        
        # Kontrollera om vi körs på Android
        if 'ANDROID_STORAGE' in os.environ:
            return 'android'
        
        # Kontrollera om vi körs på iOS (använder kivy.ios om tillgänglig)
        try:
            import kivy.ios
            return 'ios'
        except ImportError:
            pass
        
        # Annars returnera desktop-plattform
        return system.lower()  # 'windows', 'linux', 'darwin' (macOS)
    
    def show_notification(self, title, message, importance="default"):
        """
        Visar en systemnotifikation baserat på plattform.
        
        Parametrar:
            title (str): Notifikationens titel
            message (str): Notifikationens detaljerade meddelande
            importance (str): Prioritet/viktighet ('default', 'high', 'critical')
        """
        # Skapa en closure för att fånga parametrarna
        def _show_platform_notification(dt, t=title, m=message, i=importance):
            if self.platform == 'android':
                self._show_android_notification(t, m, i)
            elif self.platform == 'ios':
                self._show_ios_notification(t, m, i)
            else:
                self._show_desktop_notification(t, m, i)
        
        # Schemalägga notifikationen på huvudtråden
        Clock.schedule_once(_show_platform_notification, 0)
    
    def _show_android_notification(self, title, message, importance):
        """Visar en notifikation på Android"""
        try:
            from jnius import autoclass
            
            # Importera Android-klasser
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Context = autoclass('android.content.Context')
            NotificationBuilder = autoclass('android.app.Notification$Builder')
            NotificationManager = autoclass('android.app.NotificationManager')
            
            # Hämta context och notifikationshanterare
            context = PythonActivity.mActivity
            notification_manager = context.getSystemService(Context.NOTIFICATION_SERVICE)
            
            # Skapa notifikation
            builder = NotificationBuilder(context)
            builder.setContentTitle(title)
            builder.setContentText(message)
            builder.setSmallIcon(context.getApplicationInfo().icon)
            
            # Visa notifikation
            notification_manager.notify(1, builder.build())
            
            print(f"Android-notifikation visad: {title}")
        except Exception as e:
            print(f"Kunde inte visa Android-notifikation: {e}")
            # Fallback till konsolloggning
            print(f"NOTIFIKATION: {title} - {message}")
    
    def _show_ios_notification(self, title, message, importance):
        """Visar en notifikation på iOS"""
        try:
            # Här skulle vi använda pyobjus för iOS-notifikationer
            # Detta kräver iOS-specifik implementering
            
            # För tillfället loggar vi bara till konsolen
            print(f"iOS-notifikation skulle visas: {title} - {message}")
        except Exception as e:
            print(f"Kunde inte visa iOS-notifikation: {e}")
            # Fallback till konsolloggning
            print(f"NOTIFIKATION: {title} - {message}")
    
    def _show_desktop_notification(self, title, message, importance):
        """Visar en notifikation på desktop (Windows, macOS, Linux)"""
        try:
            # Försök använda plyer för plattformsoberoende notifikationer
            from plyer import notification
            
            notification.notify(
                title=title,
                message=message,
                app_name="Destillationsövervakare",
                timeout=10  # Sekunder att visa notifikationen
            )
            
            print(f"Desktop-notifikation visad: {title}")
        except Exception as e:
            print(f"Kunde inte visa desktop-notifikation: {e}")
            # Fallback till konsolloggning
            print(f"NOTIFIKATION: {title} - {message}")