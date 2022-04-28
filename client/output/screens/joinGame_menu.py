from ast import Mult
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from client.MultiplayerGame import MultiplayerGame
from kivy.app import App
from kivy.clock import Clock


Builder.load_file("client/output/screens/joinGame_menu.kv")

class JoinGame(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        
    def join(self):
        self.app.instanciate_MultiKS(name=self.ids.gameName.text, worldVersion_id=None, on_collision=self.on_Collision, changeLabelText=self.changeLabelText)
        
    def changeLabelText(self, message, time = 5) -> None:
        """Mise à jour puis suppession du message d'erreur à afficher après un temps <time>"""
        self.ids.labelID.text = message
        Clock.schedule_once(self.clearLabelText, time)

    def clearLabelText(self, dt) -> None:
        """Vidage du message d'erreur après un temps <dt> donné"""
        self.ids.labelID.text = ""  
        
    def on_Collision(self):
        pass