import os
import pickle
from logging import info, warning

import requests
from client.MultiplayerGame import MultiplayerGame
from client.output.outputFactory import OutputFactory
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex, rgba

from ..SingleplayerGame import SingleplayerGame
from . import MyScreenManager
from .screens.InGameScreen import KS_screen

######################## App de lancement de kivy ########################


class MenuApp(App):
    manager = ObjectProperty(None)
    soundEnabled = True
    cookiesPath = "client/cookies"
    # server = "https://lj44.ch"
    server = "https://test.lj44.ch"
    # server = "http://localhost:5044"

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
        return self.manager

    def instanciate_SoloKS(self, world, on_collision, changeLabelText):
        """Création de tout ce qui est nécessaire à une partie en solo"""
        if self.manager.has_screen("Kart_Simulator"):
            screen = self.manager.get_screen("Kart_Simulator")
            self.manager.remove_widget(screen)
        self.game_instance = (
            KS_screen()
        )  # Création du Screen qui acquillera le canvas où sera affichée la partie

        output = OutputFactory(
            widget=self.game_instance.widget,
            max_width=self.windowSize()[0],
            max_height=self.windowSize()[1],
            POV=self.get_userSettings()["pov"],
        )  # Crée la Factory qui gèrera tous les outputs
        self.game = SingleplayerGame(
            world=world,
            output=output,
            onCollision=on_collision,
            changeLabelText=changeLabelText,
            parentScreen=self.game_instance,
        )  # Création de la partie
        if self.game._game:
            self.game._game.callOutput()  # Appel d'une instance de l'output afin d'afficher le circuit derrière l'animation
            self.game_instance.startingAnimation(start_theGame=self.game.start_theGame)

    def instanciate_MultiKS(self, name, worldVersion_id, on_collision, changeLabelText):
        """Création de tout ce qui est nécessaire à une partie en multijoueur"""
        if self.manager.has_screen("Kart_Simulator"):
            screen = self.manager.get_screen("Kart_Simulator")
            self.manager.remove_widget(screen)
        self.game_instance = KS_screen()

        output = OutputFactory(
            widget=self.game_instance.widget,
            max_width=self.windowSize()[0],
            max_height=self.windowSize()[1],
            POV=self.get_userSettings()["pov"],
        )
        self.game = MultiplayerGame(
            session=self.session,
            server=self.server,
            name=name,
            output=output,
            onCollision=on_collision,
            worldVersion_id=worldVersion_id,
            changeLabelText=changeLabelText,
            parentScreen=self.game_instance,
        )
        # self.game._game.callOutput()       # Appel d'une instance de l'output afin d'afficher le circuit derrière l'animation
        # self.game_instance.startingAnimation(start_theGame=self.game.start_theGame)

    def start_ks(self):
        """Affichage de la partie"""
        self.manager.add_widget(self.game_instance)
        self.manager.push("Kart_Simulator")

    def windowSize(self):
        return Window.size

    def clearLabelText(self, label, dt):
        """Vidage du message d'erreur après un temps donné"""
        label.text = ""

    # def changeLabelText(self, labelText):
    #     """Mise à jour puis suppession du message d'erreur à afficher"""
    #     self.errorLabel.text += labelText + "\n"
    #     Clock.schedule_once(self.clearLabelText, 2)

    def clear_game(self):
        """Nettoyage de la partie finie"""
        if self.game_instance:
            if isinstance(self.game, SingleplayerGame):
                self.game.save()
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

    def set_userSettings(self, userSettings: dict) -> None:
        """Enregistre les settings et tente de les syncroniser"""
        try:
            self.userSettings = self.session.put(
                self.server + "/auth/myaccount/kart.json", userSettings
            ).json()
        except requests.ConnectionError:
            self.userSettings = userSettings
        else:
            if self.userSettings.get("error") == 401:
                # échec car le joueur n'est pas connecté
                self.userSettings = userSettings  # Enregistrement des changements pas global, mais dans l'instance de l'app lancée.

    def update_userSettings(self) -> None:
        """Met à jour les information relatives aux paramètres du joueur connecté."""
        try:
            self.userSettings = self.session.get(
                self.server + "/auth/myaccount/kart.json", timeout=1
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

    def logOut(self) -> None:
        """Déconnecte le joueur connecté."""
        self.session.get(self.server + "/auth/logout")
        self.update_userSettings()
        self._isLogged = False
        with open(self.cookiesPath, "wb") as f:
            pickle.dump(self.session.cookies, f)

    def is_logged(self) -> bool:
        """Retourne vrai si un utilisateur est connecté à son compte."""
        return self._isLogged
