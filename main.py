import os
from kivy.logger import Logger, LOG_LEVELS

# Logger.setLevel(LOG_LEVELS["warning"])

from logging import info, warning
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
from InGameScreen import KS_screen

import requests, pickle

######################## App de lancement de kivy ########################


class MenuApp(App):
    manager = ObjectProperty(None)
    soundEnabled = True
    cookiesPath = "client/cookies"
    server = "http://localhost:5000"

    _isLogged: bool = True

    def __init__(self, **kwargs):
        """L'application kivy qui gère toute l'interface graphique"""
        super().__init__(**kwargs)
        self.game_instance = None
        self.session = requests.Session()
        try:
            with open(self.cookiesPath, "rb") as f:
                self.session.cookies.update(pickle.load(f))
        except FileNotFoundError:
            self._isLogged = False
        except EOFError:
            self._isLogged = False
            os.remove(self.cookiesPath)
            warning("Deleted corrupted cookies")
        except pickle.UnpicklingError:
            self._isLogged = False
            os.remove(self.cookiesPath)
            warning("Deleted corrupted cookies")
        self.update_userSettings()

    def build(self):
        """Création du manager qui gèrera les screens et de l'espace qui affichera les éventuelles erreurs"""
        Window.clearcolor = get_color_from_hex("#ffffff")
        self.icon = "client/Images/kart.png"
        self.manager = MyScreenManager()
        with self.manager.screens[0].canvas:
            self.errorLabel = Label(
                bold=True,
                underline=True,
                font_size=32,
                text="",
                pos=(Window.width / 2 - 50, Window.height / 2 - 10),
                color=(1, 1, 1, 0.5),
            )
        return self.manager

    def instanciate_ks(self, world, POV):
        """Création du support de la partie et de ses attributs:
        monde choisi ainsi que la taille de la fenêtre"""

        if self.isWorldChosen(world):
            if self.manager.has_screen("Kart_Simulator"):
                screen = self.manager.get_screen("Kart_Simulator")
                self.manager.remove_widget(screen)
            self.game_instance = KS_screen(world=world, POV=POV)
        elif not self.isWorldChosen(world):
            self.errorLabel.text += "Choose a world before playing !\n"
            Clock.schedule_once(self.popErrorScreen, 2)

    def start_ks(self):
        """Affichage de la partie"""
        self.manager.push("Kart_Simulator")

    def windowSize(self):
        return Window.size

    def popErrorScreen(self, dt):
        """Vidage du message d'erreur après un temps donné"""
        self.errorLabel.text = ""

    def changeLabelText(self, labelText):
        """Mise à jour puis suppession du message d'erreur à afficher"""
        self.errorLabel.text += labelText + "\n"
        Clock.schedule_once(self.popErrorScreen, 2)

    def clear_game(self):
        """Nettoyage de la partie finie"""
        if self.game_instance:
            self.game_instance.quit()
            self.game_instance = None

    def ButtonSound(self):
        """Crée le son produit par un bouton si l'utilisateur n'a pas disactivé les effets sonores"""
        if self.soundEnabled:
            sound = SoundLoader.load("client/sounds/ButtonClick2.wav")
            sound.volume = 0.25
            sound.play()

    def isWorldChosen(self, world):
        """Retourne vrai si un monde a été choisi"""
        return not isinstance(world, StringProperty)

    def changeSoundMode(self, widget: Button):
        """Active ou désactive les effets sonores"""
        self.soundEnabled = not self.soundEnabled
        if self.soundEnabled:
            widget.text = "Mute sounds"
        else:
            widget.text = "Unmute sounds"

    def get_userSettings(self):
        """Retourne le dictionnaire contenant les information relatives aux paramètres du joueur connecté."""
        return self.userSettings

    def set_userSettings(self, userSetting: dict) -> None:
        """Enregistre les settings et tente de les syncroniser"""
        try:
            self.userSettings = self.session.put(
                self.server + "/auth/myaccount/kart.json", userSetting
            )
        except requests.ConnectionError:
            self.userSettings = userSetting
        else:
            if self.userSettings.get("error") == 401:
                # échec car le joueur n'est pas connecté
                self.userSettings = userSetting

    def update_userSettings(self) -> None:
        """Met à jour les information relatives aux paramètres du joueur connecté."""
        try:
            self.userSettings = self.session.get(
                self.server + "/auth/myaccount/kart.json"
            ).json()
        except requests.ConnectionError:
            self.userSettings = {
                "kart": "Green_kart",
                "music": "No Music",
                "pov": "Third Person",
                "username": "Anonyme user",
                "volume": 1,
            }
            info("Client offline")
        else:
            if self.userSettings.get("error") == 401:
                self._isLogged = False
                self.userSettings = {
                    "kart": "Green_kart",
                    "music": "No Music",
                    "pov": "Third Person",
                    "username": "Anonyme user",
                    "volume": 1,
                }

    def is_logged(self) -> bool:
        """Retourne vrai si un utilisateur est connecté à son compte."""
        return self._isLogged


from kivy.config import Config
from kivy.core.window import Window

# Window.fullscreen = 'auto'
Config.set("kivy", "exit_on_escape", "0")
Config.set("input", "mouse", "mouse,multitouch_on_demand")


MenuApp().run()

# ##########################################################################
