from kivy.app import App
from kivy.clock import Clock
from kivy.core import window
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex, rgba
from kivy.core.window import Window
from kart_simulator import MainWidget
from kivy.core.audio import SoundLoader
from kivy.graphics import Rectangle, Color
from kivy.uix.label import Label

from navigation_screen_manager import MyScreenManager
from layouts import KS_screen


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
    
    def start_ks(self, world, music):
        self.windowSize = Window.size
        if self.isWorldChosen(world):
            self.world = world
            self.music = music
            if self.manager.has_screen("Kart_Simulator"):
                screen = self.manager.get_screen("Kart_Simulator")
                self.manager.remove_widget(screen)
            
            self.game_instance = KS_screen(world,music)
            self.manager.add_widget(self.game_instance)
            self.manager.push("Kart_Simulator")
            
        elif not self.isWorldChosen(world):
            with self.manager.canvas:
                self.errorLabel=Label(bold=True,underline=True,font_size=100,text="Choose a world before playing !",pos=(Window.width/2-50,Window.height/2-10),color=(1,1,1,.5))
            # self.manager.canvas.clear(self.errorLabel)            
            Clock.schedule_once(self.popErrorScreen, 2)
            
    def popErrorScreen(self,dt):
        self.errorLabel.text = ""
        
    def clear_game(self):
        if self.game_instance:
            self.game_instance.quit()
            self.game_instance = None
            
    def ButtonSound(self):
        sound = SoundLoader.load('client/sounds/ButtonClick2.wav')
        sound.volume = 0.25
        sound.play()

    def isWorldChosen(self,world):
        return not isinstance(world,StringProperty)






from kivy.config import Config
from kivy.core.window import Window
# Window.fullscreen = 'auto'
Config.set('kivy', 'exit_on_escape', '0')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


MenuApp().run()

##########################################################################