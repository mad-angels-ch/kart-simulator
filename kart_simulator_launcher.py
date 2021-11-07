from kivy.app import App
from kivy.core import window
from kivy.properties import StringProperty, ObjectProperty
from kivy.utils import get_color_from_hex, rgba
from kivy.core.window import Window
from kart_simulator import MainWidget



from navigation_screen_manager import MyScreenManager
from layouts import KS_screen, KS



######################## App de lancement de kivy ########################



class MenuApp(App):
    manager = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        Window.clearcolor = get_color_from_hex("#ffffff")
        self.manager = MyScreenManager()
        return self.manager
        # return MainWidget()

    def start_ks(self):
        if self.manager.has_screen("Kart_Simulator"):
            screen = self.manager.get_screen("Kart_Simulator")
            self.manager.remove_widget(screen)
        game_instance = KS_screen()
        self.manager.add_widget(game_instance)
        self.manager.push("Kart_Simulator")

        
        


# from kivy.core.window import Window
# Window.fullscreen = True

# from kivy.config import Config
# Config.set('graphics', 'fullscreen', 1)

MenuApp().run()

##########################################################################