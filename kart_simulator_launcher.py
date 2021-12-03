from kivy.app import App
from kivy.core import window
from kivy.properties import StringProperty, ObjectProperty
from kivy.utils import get_color_from_hex, rgba
from kivy.core.window import Window
from kart_simulator import MainWidget
from kivy.core.audio import SoundLoader


from navigation_screen_manager import MyScreenManager
from layouts import KS_screen, KS



######################## App de lancement de kivy ########################



class MenuApp(App):
    manager = ObjectProperty(None)
    musicName = ""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_instance = None
        
    def build(self):
        Window.clearcolor = get_color_from_hex("#ffffff")
        self.manager = MyScreenManager()
        return self.manager
        # return MainWidget()

    def start_ks(self, world, music):
        self.world = world
        self.music = music
        if self.manager.has_screen("Kart_Simulator"):
            screen = self.manager.get_screen("Kart_Simulator")
            self.manager.remove_widget(screen)
        self.game_instance = KS_screen(world,music)
        self.manager.add_widget(self.game_instance)
        self.manager.push("Kart_Simulator")
        
    def clear_game(self):
        if self.game_instance:
            self.game_instance.quit()
            self.game_instance = None
        
        
            
    def ButtonSound(self):
        sound = SoundLoader.load('client/sounds/ButtonClick2.wav')
        sound.volume = 0.05
        sound.play()







from kivy.config import Config
from kivy.core.window import Window
# Window.fullscreen = 'auto'
Config.set('kivy', 'exit_on_escape', '0')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


MenuApp().run()

##########################################################################