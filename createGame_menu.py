from os import listdir, path
from typing import Tuple
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.graphics.transformation import Matrix
import game
from game.objects.ObjectFactory import ObjectCountError
from client.output import OutputFactory
from kivy.clock import Clock
Builder.load_file("createGame_menu.kv")

class CreateGame(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chosen_world = StringProperty("Choose your world")
    def changeWorldSpinnerText(self, text):
        """Change le texte affiché sur le dépliant de choix du circuit"""
        self.chosen_world = text
        
    def generateWorldsList(self):
        """Génère la liste des curcuits jouables"""
        return [world[:-5] for world in listdir("client/worlds")]
    
    def changeLabelText(self, message):
        """Mise à jour puis suppession du message d'erreur à afficher"""
        self.ids.labelID.text=message
        
    def popErrorScreen(self):
        """Vidage du message d'erreur après un temps donné"""
        self.ids.labelID.text = ""
        
    
    

class PreView(Widget):
    def __init__(self, maxSize:Tuple[float,float] = (200,200), **kwargs):
        """Widget créant le preview"""
        self.maxSize = maxSize
        super().__init__(**kwargs)

    def changePreView(self, world):
        """Change le mode de preview pour afficher le nouveau circuit"""
        # Se comporte comme MainWidget, mais n'instancie qu'une seule frame
        self.parent.parent.parent.parent.popErrorScreen()
        if not isinstance(world, StringProperty):
            self.canvas.before.clear()
            self.canvas.clear()
            self.canvas.after.clear()
            if self.parent.parent.scale != 1:
                self.parent.parent.scale = 1
                # Repositionne le ScatterLayout dans lequel se situe le preview à la position (0,0) et réinitialise son facteur scale à 1
                self.parent.parent.pos = (0,0)
            try:
                self.dataUrl = self.dataUrl = (
                    path.join("client/worlds", world) + ".json"
                )
                app = App.get_running_app()
                with open(self.dataUrl, "r", encoding="utf8") as f:
                    self.theGame = game.Game(
                        f.read(),
                        OutputFactory(self, max_width=self.maxSize[0], max_height=self.maxSize[1], POV="PreView"),
                    )

                self.theGame.callOutput()
            except ObjectCountError as OCE:
                self.parent.parent.parent.parent.changeLabelText(OCE.message())
