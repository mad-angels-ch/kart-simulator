import json
import os
import pickle
from logging import info, warning
from typing import Tuple

import requests
from client.MultiplayerGame import MultiplayerGame
from client.output.outputFactory import OutputFactory
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex

from ..SingleplayerGame import SingleplayerGame
from . import MyScreenManager
from .screens.InGameScreen import KS_screen

######################## App de lancement de kivy ########################


class MenuApp(App):
    manager = ObjectProperty(None)
    soundEnabled = True
    cookiesPath = "client/cookies"
    server = "https://lj44.ch"

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

        self.generateUpdatedWorldsList()
        self.update_userSettings()
        self.y = 0
        # Pour une raison inconnue, lors du redimensionnement d'une fenêtre (qui n'arrive normalement pas car le jeu est par défaut en plein écran),
        # kivy essaie de retrouver la "hauteur" "self.y" de cette classe alors qu'elle n'est en rien liée à l'application graphique...
        # N'ayant pas réussi à régler le problème autrement, nous avons créé la méthode to_window() et l'attribut "y" qui règlent le problème.

    def to_window(self, a, b) -> None:
        # c.f. commentaire de self.y ci-dessus
        return self.windowSize()

    def build(self):
        """Création du manager qui gèrera les screens et de l'espace qui affichera les éventuelles erreurs"""
        Window.clearcolor = get_color_from_hex("#ffffff")
        self.bind_keyboard()
        self.icon = "client/Images/kart.png"
        self.manager = MyScreenManager()
        return self.manager

    def instanciate_SoloKS(self, world, on_collision, changeLabelText) -> None:
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

    def instanciate_MultiKS(
        self, name, worldVersion_id, on_collision, changeLabelText
    ) -> None:
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

    def start_ks(self) -> None:
        """Affichage de la partie"""
        self.manager.add_widget(self.game_instance)
        self.manager.push("Kart_Simulator")

    def windowSize(self) -> Tuple[float, float]:
        return Window.size

    def clearLabelText(self, label, dt) -> None:
        """Vidage du message d'erreur après un temps donné"""
        label.text = ""

    def clear_game(self) -> None:
        """Nettoyage de la partie finie"""
        if self.game_instance:
            if isinstance(self.game, SingleplayerGame):
                self.game.save()
            self.game_instance.quit()
            self.game_instance = None

    def ButtonSound(self) -> None:
        """Crée le son produit par un bouton si l'utilisateur n'a pas disactivé les effets sonores"""
        if self.soundEnabled:
            sound = SoundLoader.load("client/sounds/ButtonClick2.wav")
            sound.volume = 0.25
            sound.play()

    def isWorldChosen(self, world) -> bool:
        """Retourne vrai si un monde a été choisi"""
        return not isinstance(world, StringProperty)

    def changeSoundMode(self, widget: Button) -> None:
        """Active ou désactive les effets sonores"""
        self.soundEnabled = not self.soundEnabled
        if self.soundEnabled:
            widget.text = "Mute sounds"
        else:
            widget.text = "Unmute sounds"

    def get_userSettings(self) -> dict:
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

    def generateUpdatedWorldsList(self) -> None:
        """Met à jour les donnés des mondes"""
        self._updating = True
        worldsInfo = {}
        try:
            worlds = self.session.get(
                self.server + "/creator/kart/worldsjson",
                params={"id": True, "worldVersion_id": True, "name": True},
            ).json()
        except requests.ConnectionError:
            self._updating = False
        else:
            for world in worlds:
                worldsInfo[world["name"]] = {
                    "id": world["id"],
                    "version_id": world["worldVersion_id"],
                }
            try:
                f = open("client/worlds.json", "r", encoding="utf8")
            except FileNotFoundError:
                f = open("client/worlds.json", "w", encoding="utf8")
                f.write("{}")
                f.close()
                f = open("client/worlds.json", "r", encoding="utf8")

            try:
                savedWorld = json.load(f)
                # mise à jour des mondes déjà téléchargés
                for name, data in savedWorld.items():
                    if name in worldsInfo:
                        if data.get("version_id", -1) != worldsInfo[name]["version_id"]:
                            with open(f"client/worlds/{name}.json", "w") as worldJSON:
                                worldJSON.write(
                                    self.session.get(
                                        f"{self.server}/creator/kart/worlds/{worldsInfo[name]['id']}/fabric"
                                    ).text
                                )
                            data["version_id"] = worldsInfo[name]["version_id"]
                    else:
                        os.remove(f"client/worlds/{name}.json")
                # téléchargement des autres
                downloadedWorlds = [world[:-5] for world in os.listdir("client/worlds")]
                for name, data in worldsInfo.items():
                    if name not in downloadedWorlds:
                        with open(f"client/worlds/{name}.json", "w") as worldJSON:
                            worldJSON.write(
                                self.session.get(
                                    f"{self.server}/creator/kart/worlds/{worldsInfo[name]['id']}/fabric"
                                ).text
                            )

            finally:
                f.close()

            with open("client/worlds.json", "w") as f:
                json.dump(worldsInfo, f)
            self._updating = False


    def bind_keyboard(self) -> None:
        self._keyboard = Window.request_keyboard(self.on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_keyboard_down)

    def on_keyboard_closed(self) -> None:
        self._keyboard.unbind(on_key_down=self.on_keyboard_down)
        self._keyboard = None
        
    def on_keyboard_down(self, keyboard, keycode, text, modifiers) -> None:
        if keycode[1] == "escape" and self.manager.current != "Kart_Simulator":
            self.manager.pop()