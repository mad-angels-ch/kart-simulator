from kivy.app import App
from kivy.clock import Clock
from kivy.core import window
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex, rgba
from kivy.core.window import Window
from kart_simulator import MainWidget
from kivy.core.audio import SoundLoader
from kivy.graphics import Rectangle, Color
from kivy.uix.label import Label
from kivy.uix.image import Image
from navigation_screen_manager import MyScreenManager
from layouts import KS_screen, Start_anim

######################## App de lancement de kivy ########################



class MenuApp(App):
    manager = ObjectProperty(None)
    musicName = ""
    soundEnabled = True
    passwords = [False,False]
    
    def __init__(self, **kwargs):
        """L'application kivy qui gère toute l'interface graphique"""
        super().__init__(**kwargs)
        self.game_instance = None
        

    def build(self):
        """Création du manager qui gèrera les screens et de l'espace qui affichera les éventuelles erreurs"""
        Window.clearcolor = get_color_from_hex("#ffffff")
        self.icon = 'client/Images/kart.png'

        self.manager = MyScreenManager()
        with self.manager.screens[0].canvas:
            self.errorLabel=Label(bold=True,underline=True,font_size=32,text="",pos=(Window.width/2-50,Window.height/2-10),color=(1,1,1,.5))
        return self.manager
    
    def start_manager(self):
        return self.manager
    
    def instanciate_ks(self, world, music, POV):
        """Création du support de la partie et de ses attributs: 
        monde et musique choisis ainsi que la taille de la fenêtre"""
        self.windowSize = Window.size
        if self.isWorldChosen(world):
            self.world = world
            self.music = music
            self.POV = POV
            if self.manager.has_screen("Kart_Simulator"):
                screen = self.manager.get_screen("Kart_Simulator")
                self.manager.remove_widget(screen)
            self.game_instance = KS_screen(self.world, self.music, self.POV)
        elif not self.isWorldChosen(world):
            self.errorLabel.text+="Choose a world before playing !\n"
            Clock.schedule_once(self.popErrorScreen, 2)
            
    def start_ks(self):
        """Affichage de la partie"""
        self.manager.push("Kart_Simulator")
        
    def popErrorScreen(self,dt):
        """Vidage du message d'erreur après un temps donné"""
        self.errorLabel.text = ""
        
    def changeLabelText(self,labelText):
        """Mise à jour puis suppession du message d'erreur à afficher"""
        self.errorLabel.text+=labelText+"\n"
        Clock.schedule_once(self.popErrorScreen, 2)
        
    def clear_game(self):
        """Nettoyage de la partie finie"""
        if self.game_instance:
            self.game_instance.quit()
            self.game_instance = None
            
    def ButtonSound(self):
        """Crée le son produit par un bouton si l'utilisateur n'a pas disactivé les effets sonores"""
        if self.soundEnabled:
            sound = SoundLoader.load('client/sounds/ButtonClick2.wav')
            sound.volume = 0.25
            sound.play()

    def isWorldChosen(self,world):
        """Retourne vrai si un monde a été choisi"""
        return not isinstance(world,StringProperty)
    
    def changeSoundMode(self, widget: Button):
        """Active ou désactive les effets sonores"""
        self.soundEnabled = not self.soundEnabled
        if self.soundEnabled:
            widget.text = "Mute sounds"
        else:
            widget.text = "Unmute sounds"
        





from kivy.config import Config
from kivy.core.window import Window
Window.fullscreen = 'auto'
Config.set('kivy', 'exit_on_escape', '0')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


MenuApp().run()

# ##########################################################################
