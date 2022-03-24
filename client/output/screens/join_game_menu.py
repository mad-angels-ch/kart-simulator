from ast import Mult
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from client.MultiplayerGame import MultiplayerGame
from kivy.app import App

Builder.load_file("client/output/screens/join_game_menu.kv")

class JoinGame(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        
    def join(self):
        MultiplayerGame(session=self.app.session, server=self.app.server, name=self.ids.gameName, output=None, onCollision=self.on_Collision, errorLabel=self.ids.ErrorLabel)
        
    def on_Collision(self):
        pass