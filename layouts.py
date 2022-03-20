from io import TextIOWrapper
from kivy.graphics.transformation import Matrix
from logging import warning
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
import requests, json, os, threading
from kart_simulator import game, path, Rectangle, Color
from os import path, listdir, write
from posixpath import abspath
from re import S
import time
import os.path
from typing import Dict, List
from kivy.core.window import Window
from lib import Point
try:
    import client.worlds
except ModuleNotFoundError:
    os.makedirs("client/worlds")
    import client.worlds
from game.objects import *
import game
from kivy.app import App
from kivy.utils import get_color_from_hex, rgba
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.properties import Clock
from kivy.properties import StringProperty
from client.output import OutputFactory
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.utils import rgba
from game.objects.ObjectFactory import ObjectCountError
from kart_simulator import MainWidget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.core.audio import SoundLoader
from kivy.uix.dropdown import DropDown
from action_bar import BoxLayoutWithActionBar
from game.objects.fill.Hex import Hex
from game.objects.fill.Pattern import Pattern
from kivy.uix.image import Image
from kivy.animation import Animation

import pickle

#################### Gestion des différents screens ###################


class NavigationScreenManager(ScreenManager):
    """Classe parente du manager qui gère les entrées et sorties des screens"""

    screen_stack = []

    def push(self, screen_name):
        """Entrée d'un nouveau screen"""
        if screen_name not in self.screen_stack:
            self.screen_stack.append(self.current)
            self.transition.direction = "left"
            self.current = screen_name

    def pop(self):
        """Sortie du dernier screen"""
        if len(self.screen_stack) > 0:
            screen_name = self.screen_stack[-1]
            del self.screen_stack[-1]
            self.transition.direction = "right"
            self.current = screen_name


class MyScreenManager(NavigationScreenManager):
    """Manager qui gère les entrées et sorties des screens"""
    pass






class MainMenu2(FloatLayout):
    def __init__(self, **kwargs):
        """Menu principal du jeu"""
        super().__init__(**kwargs)
        self.chosen_world = StringProperty("Choose your world")
        self.chosen_music = StringProperty("Choose your music")
        self.chosen_POV = StringProperty("Choose your Point Of View")

    def changeWorldSpinnerText(self, text):
        """Change le texte affiché sur le dépliant de choix du circuit"""
        self.chosen_world = text

    def changeMusicSpinnerText(self, text):
        """Change le texte affiché sur le dépliant de choix de la musique"""
        self.chosen_music = text
        
    def changePOVSpinnerText(self, text):
        """Change le texte affiché sur le dépliant de choix du point de vue"""
        self.chosen_POV = text

    def generateWorldsList(self):
        """Génère la liste des curcuits jouables"""
        return [world[:-5] for world in listdir("client/worlds")]

    def generateMusicsList(self):
        """Génère la liste des musiques jouables"""
        music_list = list(music[:-4] for music in listdir("client/sounds/music"))
        music_list.append("No music")
        return music_list


class UpdateWorlds(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_text_validate(self, widget):
        if widget.text == "Vive le flipper":
            App.get_running_app().manager.push("EG1")



##########################################################################


class PasswordScreen(FloatLayout):
    def __init__(self, nbr=0, **kw):
        self.nbr = nbr
        self.app = App.get_running_app()
        super().__init__(**kw)

    def on_text_validate(self, widget):
        self.app.passwords[self.nbr - 1] = False
        if self.nbr == 1:
            self.app.passwords[self.nbr] = False
            if widget.text == "Noe est le plus beau...":
                self.app.passwords[self.nbr - 1] = True
            self.app.manager.push("EG2")

        elif self.nbr == 2:
            if widget.text == "...mais Lorin le suit de près":
                self.app.passwords[self.nbr - 1] = True
            for i in range(3):
                self.app.manager.pop()
        widget.text = "Type the secret password:"
        if self.app.passwords[0] and self.app.passwords[1]:
            self.app.instanciate_ks(world="client/easteregg.json", music="No music", POV="Thrid Person")







# from player import *

class GameConnection(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def main(self, create, join):
        """Create a player of the ks multiplayer"""
        username = self.ids.username.text
        password = self.ids.password.text
        session = requests.Session()
        data = {"username": username, "password": password}
        response = session.post("http://localhost:5000/auth/login", data=data).text
        title = "<title>"
        pos = response.find(title) + len(title)
        error = "Error | "
        if response[pos : pos + len(error)] == error:
            self.ids.errors.text="Wrong username of password. Try again."
        # else:
            # sio = Client()
            # sio = Client(logger=True, engineio_logger=True)
            # sio.register_namespace(MultiplayerGame("/kartmultiplayer", create="Test", join=""))
            # try:
            #     # sio.connect("http://localhost:5000", namespaces="/kartmultiplayer")
            # except BaseException as e:
            #     self.ids.errors.text=str(e)
    
    
    
    
# class JoinGame(FloatLayout):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.username = self.ids.username.text
#         self.password = self.ids.password.text
        
#     def main(self):
#         """Create a player of the ks multiplayer"""
#         session = requests.Session()
#         data = {"username": self.username, "password": self.password}
#         response = session.post("http://localhost:5000/auth/login", data=data).text
#         title = "<title>"
#         pos = response.find(title) + len(title)
#         error = "Error | "
#         if response[pos : pos + len(error)] == error:
#             self.ids.errors.text="Wrong username of password. Try again."
#             raise click.Abort()

#         sio = Client()
#         # sio = Client(logger=True, engineio_logger=True)
#         # sio.register_namespace(MultiplayerGame("/kartmultiplayer", create, join))
#         try:
#             sio.connect("http://localhost:5000", namespaces="/kartmultiplayer")
#         except BaseException as e:
#             click.echo(e)
#             sys.exit()





from functools import partial
from kivy.uix.popup import Popup


class LogInQuestion(Popup):
    """Classe qui demande à l'utilisateur s'il veut se connecter à son compte ou non, puis se détruit."""
    def __init__(self, parent, **kwargs):
        super().__init__(title="You are not logged in.",**kwargs)
        self.pos_hint = {"center_x":.5, "center_y": .7}
        self.size_hint = (.5,.2)
        box1 = BoxLayout(orientation='vertical')
        app = App.get_running_app()
        box1.add_widget(Label(text = "Do you want to log in ?"))
        box2 = BoxLayout(orientation = "horizontal")
        box1.add_widget(box2)
        box2.add_widget(Button(text = "Yes", on_release = lambda screen:app.manager.push("LogIn"), on_press = lambda s: parent.remove_widget(self)))
        box2.add_widget(Button(text = "No", on_release = lambda screen:app.manager.push("Playingmode"), on_press = lambda s: parent.remove_widget(self)))
        self.content = box1