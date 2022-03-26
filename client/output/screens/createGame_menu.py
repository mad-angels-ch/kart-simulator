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
import requests, json, os, threading
from kivy.core.audio import SoundLoader
from functools import partial
from client.MultiplayerGame import MultiplayerGame
from client.output.kart_simulator import MainWidget
import json

Builder.load_file("client/output/screens/createGame_menu.kv")


class CreateGame(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chosen_world = StringProperty("Choose your world")
        self.app = App.get_running_app()

    def changeWorldSpinnerText(self, text) -> None:
        """Change le texte affiché sur le dépliant de choix du circuit"""
        self.chosen_world = text

    def generateWorldsList(self) -> list:
        """Génère la liste des curcuits jouables"""
        return [world[:-5] for world in listdir("client/worlds")]

    def changeLabelText(self, message) -> None:
        """Mise à jour puis suppession du message d'erreur à afficher"""
        self.ids.labelID.text = message

    def popErrorScreen(self) -> None:
        """Vidage du message d'erreur après un temps donné"""
        self.ids.labelID.text = ""

    def create(self) -> None:
        """Crée la partie multijoueur."""
        try:
            name = (
                self.children[0].children[1].text
            )  # Récupération  du texte pour le nom à partir d'un "TextInput" ajouté dans "MyScreenManager"
        except:
            self.app.instanciate_ks(world=self.chosen_world, POV = "Third Person")
        with open(
            "client/worlds.json", "r", encoding="utf8"
        ) as f:  # Lecture et transformation du ficher worlds.json pour y accéder sous la forme d'un dictionnaire
            worldVersion_id = json.loads(f.read())[self.chosen_world]["version_id"]
        MultiplayerGame(
            session=self.app.session,
            server=self.app.server,
            name=name,
            output=OutputFactory(
                self,
                frame_callback=self.frame_callback,
                max_width=self.app.windowSize()[0],
                max_height=self.app.windowSize()[1],
                POV="Third Person",
            ),
            onCollision=self.on_Collision,
            worldVersion_id=worldVersion_id,
            errorLabel=self.ids["labelID"],
        )

    def on_Collision(self) -> None:
        pass

    def frame_callback(self) -> None:
        pass

    def on_Collision(self):
        pass


class PreView(Widget):
    def __init__(self, maxSize: Tuple[float, float] = (200, 200), **kwargs):
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
                self.parent.parent.pos = (0, 0)
            try:
                self.dataUrl = self.dataUrl = (
                    path.join("client/worlds", world) + ".json"
                )
                app = App.get_running_app()
                with open(self.dataUrl, "r", encoding="utf8") as f:
                    self.theGame = game.Game(
                        f.read(),
                        OutputFactory(
                            self,
                            max_width=self.maxSize[0],
                            max_height=self.maxSize[1],
                            POV="PreView",
                        ),
                    )

                self.theGame.callOutput()
            except ObjectCountError as OCE:
                self.parent.parent.parent.parent.changeLabelText(OCE.message())


class UpdateWorldButton(Button):
    def __init__(self, **kwargs):
        """Bouton qui met à jour dynamiquement la liste des mondes jouables"""
        super().__init__(**kwargs)
        self._updating = False
        self.app = App.get_running_app()

    def generateUpdatedWorldsList(self, updateWorlds_output, worlds_spinner):
        """Met à jour les donnés des mondes et met l'affichage à jour"""
        if self._updating:
            self.text = "It's already updating!"
        else:
            self._updating = True
            threading.Thread(
                target=self.generateUpdatedWorldsListTask,
                args=(updateWorlds_output, worlds_spinner),
            ).start()

    def generateUpdatedWorldsListTask(self, updateWorlds_output, worlds_spinner):
        """Récupère les données des mondes et met à jour l'affichage"""
        updateWorlds_output.text = "\nUpdating the worlds ...\n"
        worldsInfo = {}
        try:
            worlds = self.app.session.get(
                self.app.server + "/creator/kart/worldsjson",
                params={"id": True, "worldVersion_id": True, "name": True},
            ).json()
        except requests.ConnectionError:
            updateWorlds_output.text += "ERROR: The server in unreachable, please check your internet connection and try again."
            self._updating = False
            self.text = "Update the worlds now"
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
                            updateWorlds_output.text += f"Updating world {name} ... "
                            with open(f"client/worlds/{name}.json", "w") as worldJSON:
                                worldJSON.write(
                                    self.app.session.get(
                                        f"{self.app.server}/creator/kart/worlds/{worldsInfo[name]['id']}/fabric"
                                    ).text
                                )
                            updateWorlds_output.text += "done!\n"
                            data["version_id"] = worldsInfo[name]["version_id"]
                    else:
                        updateWorlds_output.text += f"Deleting world {name} ... "
                        os.remove(f"client/worlds/{name}.json")
                        updateWorlds_output.text += "done!\n"
                # téléchargement des autres
                for name, data in worldsInfo.items():
                    if name not in savedWorld:
                        updateWorlds_output.text += f"Downloading world {name} ... "
                        with open(f"client/worlds/{name}.json", "w") as worldJSON:
                            worldJSON.write(
                                self.app.session.get(
                                    f"{self.app.server}/creator/kart/worlds/{worldsInfo[name]['id']}/fabric"
                                ).text
                            )
                        updateWorlds_output.text += "done!\n"

            finally:
                f.close()

            with open("client/worlds.json", "w") as f:
                json.dump(worldsInfo, f)

            worlds_spinner.value = [world[:-5] for world in listdir("client/worlds")]
            updateWorlds_output.text += "All worlds are up to date!"
            self._updating = False
            Clock.schedule_once(partial(self.clearLabelText, updateWorlds_output), 4)
            self.text = "Update the worlds now"
            if App.get_running_app().soundEnabled:
                sound = SoundLoader.load("client/sounds/success-sound-effect.mp3")
                sound.volume = 0.5
                sound.play()

    def clearLabelText(self, label, dt):
        # print("oK")
        label.text = ""