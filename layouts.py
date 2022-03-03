from io import TextIOWrapper
from kivy.graphics.transformation import Matrix
from logging import warning
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout
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


class EndGameMode(FloatLayout):
    """Menu de fin de partie"""
    pass


class PauseMode(FloatLayout):
    def __init__(self, width, height, music, **kwargs):
        """Menu de pause"""

        self.chosen_music = str(music)
        self.width = width
        self.height = height
        super().__init__(**kwargs)

    def changeMusicSpinnerText(self, text):
        """Change le texte à afficher sur le dépliant de choix de la musique"""
        self.chosen_music = text

    def generateMusicsList(self):
        """Génère la liste des musiques disponibles"""
        music_list = list(music[:-4] for music in listdir("client/sounds/music"))
        music_list.append("No music")
        return music_list


class KS_screen(Screen):
    def __init__(self, world, music, POV, **kw):
        """Screen responsable d'afficher la partie"""
        self.musicName = self.get_musicName(music)
        super().__init__(**kw)

        self.app = App.get_running_app()
        self.world = world
        self.POV = POV
        # Instantiation du canvas de jeu
        self.game = MainWidget(self.world, POV=self.POV, parentScreen=self)
        if self.game.theGame:
            self.startMusic()
            self.ids.noActionBar.add_widget(self.game)
            # self.start_button = Button(text="start The game!", size_hint=(0.25, 0.1))
            # self.start_button.bind(on_press=self.startingAnimation)
            # self.ids.noActionBar.add_widget(self.start_button)
            self.game.theGame.callOutput()
            self.startingAnimation()

    def quit(self):
        """Nettoyage du canvas de jeu après la partie"""
        self.game.clear()

    def pauseMode(self):
        """Appel du mode de pause"""
        if self.musicName:
            self.pauseMusic()

        self.game.my_clock.unschedule(self.game.nextFrame)
        self.pauseMenu = PauseMode(
            width=Window.width, height=Window.height, music=self.musicName
        )
        self.add_widget(self.pauseMenu)

    def endGameMode(self, message):
        """Appel du mode de fin de partie"""
        if self.musicName:
            self.pauseMusic()

        self.game.my_clock.unschedule(self.game.nextFrame)
        self.endGameMenu = EndGameMode()
        self.endGameMenu.ids.gameOverLabel_id.text = message
        anim = (
            Animation(font_size=74, duration=0.1)
            + Animation(font_size=120, duration=1)
            + Animation(font_size=120, duration=0.1)
            + Animation(font_size=74, duration=1)
        )
        anim.repeat = True
        anim.start(self.endGameMenu.ids.gameOverLabel_id)
        self.add_widget(self.endGameMenu)

    def begin_game(self, dt):
        """Démarrage de la partie"""
        self.game.start_theGame()

    def startingAnimation(self):
        """Création et affichage de l'animation de début de partie"""
        # self.ids.noActionBar.remove_widget(self.start_button)
        start_animation3 = Label(
            text="3", font_size=0, halign="center", color=(0, 1, 0, 1)
        )
        start_animation2 = Label(
            text="2", font_size=0, halign="center", color=(0, 1, 0, 1)
        )
        start_animation1 = Label(
            text="1", font_size=0, halign="center", color=(0, 1, 0, 1)
        )
        start_animationGO = Label(
            text="GOOOO!!!!", font_size=0, halign="center", color=(0, 1, 0, 1)
        )

        self.ids.animationLayout.add_widget(start_animation3)
        self.ids.animationLayout.add_widget(start_animation2)
        self.ids.animationLayout.add_widget(start_animation1)
        self.ids.animationLayout.add_widget(start_animationGO)
        anim = (
            Animation(font_size=74, duration=0.5)
            + Animation(font_size=200, duration=0.5)
            + Animation(font_size=0, duration=0.5)
        )
        anim.start(start_animation3)
        anim = (
            Animation(duration=1.5)
            + Animation(font_size=74, duration=0.5)
            + Animation(font_size=200, duration=0.5)
            + Animation(font_size=0, duration=0.5)
        )
        anim.start(start_animation2)
        anim = (
            Animation(duration=3)
            + Animation(font_size=74, duration=0.5)
            + Animation(font_size=200, duration=0.5)
            + Animation(font_size=0, duration=0.5)
        )
        anim.start(start_animation1)
        anim = (
            Animation(duration=4.5)
            + Animation(font_size=74, duration=0.5)
            + Animation(font_size=400, duration=0.5)
            + Animation(font_size=0, duration=0.5)
        )
        anim.start(start_animationGO)
        # Appel d'une instance de l'output afin d'afficher le circuit derrière l'animation
        Clock.schedule_once(self.begin_game, 6)

    def end_game(self, endGameMessage=""):
        """Appel du mode de fin de partie"""
        self.endGameMode(endGameMessage)
        self.game.play = -1

    def resumeGame(self, new_music):
        """Reprise de la partie à la fin de la pause"""
        self.resumeMusic()

        self.game.play = 1
        self.game.my_clock.schedule_interval(self.game.nextFrame, 1 / self.game.fps)
        self.remove_widget(self.pauseMenu)

    def startMusic(self):
        """Initialisation de la musique (avec répétitions)"""

        if self.app.soundEnabled:
            if self.musicName in list(music[:-4] for music in listdir("client/sounds/music")):
                musicPath = path.join("client/sounds/music", self.musicName) + ".wav"
                self.music = SoundLoader.load(musicPath)
                # self.music_pos = 0
                self.music.volume = 1
                self.music.play()
                # self.music.seek(self.music_pos)
                self.music.loop = True

    def changeMusic(self, new_music):
        """Changement de la musique"""
        self.musicName = new_music

    def pauseMusic(self):
        """Arrêt de la musique lors du mode pause"""
        try:
            # self.music_pos = self.music.get_pos()     #Bug connu dans la class "sounds" de kivy, indisponible pour l'instant...
            self.music.stop()
            # self.music.loop = False
        except:
            pass

    def resumeMusic(self):
        """Reprend la musique après une pause"""
        self.startMusic()

    def get_musicName(self, music):
        if isinstance(music, StringProperty):
            return music.defaultvalue
        else:
            return music


class PreView(Widget):
    def __init__(self, **kwargs):
        """Widget créant le preview"""
        super().__init__(**kwargs)
        self.previewMode = False

    def changePreView(self, world):
        """Change le mode de preview pour afficher le nouveau circuit"""
        # Se comporte comme MainWidget, mais n'instancie qu'une seule frame
        if not isinstance(world, StringProperty):
            self.canvas.before.clear()
            self.canvas.clear()
            self.canvas.after.clear()
            if self.parent.parent.scale != 1 and self.previewMode:
                # Repositionne le ScatterLayout dans lequel se situe le preview à la position (0,0) et réinitialise son facteur scale à 1
                self.parent.parent.pos = (0,0)
                self.parent.parent.apply_transform(trans=Matrix().scale(1/self.theGame._output._scale, 1/self.theGame._output._scale, 1/self.theGame._output._scale),anchor=(0,0))
            if self.previewMode:
                try:
                    self.dataUrl = self.dataUrl = (
                        path.join("client/worlds", world) + ".json"
                    )
                    app = App.get_running_app()
                    with open(self.dataUrl, "r", encoding="utf8") as f:
                        self.theGame = game.Game(
                            f.read(),
                            OutputFactory(self, max_width=200, max_height=200, POV="PreView"),
                        )

                    self.theGame.callOutput()
                except ObjectCountError as OCE:
                    app.changeLabelText(OCE.message())

    def updatePreviewMode(self):
        """Met à jour le mode de preview: vrai si il faut afficher un preview et faux sinon"""
        self.previewMode = not self.previewMode


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


class UpdateWorldButton(Button):
    def __init__(self, **kwargs):
        """Bouton qui met à jour dynamiquement la liste des mondes jouables"""
        super().__init__(**kwargs)
        self._updating = False

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
        session = requests.Session()
        try:
            worlds = session.get(
                "https://lj44.ch/creator/kart/worldsjson",
                params={"id": True, "version": True, "name": True},
                timeout=1,
            )
        except requests.ConnectionError:
            updateWorlds_output.text += "ERROR: The server in unreachable"
            self._updating = False
            self.text = "Update the worlds now"
        else:
            for world in worlds.json():
                worldsInfo[world["name"]] = {"id": world["id"], "version": world["version"]}
            try:
                f = open("client/worlds.json", "r")
            except FileNotFoundError:
                f = open("client/worlds.json", "w")
                f.write("{}")
                f.close()
                f = open("client/worlds.json", "r")

            try:
                savedWorld = json.load(f)
                # mise à jour des mondes déjà téléchargés
                for name, data in savedWorld.items():
                    if name in worldsInfo:
                        if data["version"] != worldsInfo[name]["version"]:
                            updateWorlds_output.text += f"Updating world {name} ... "
                            with open(f"client/worlds/{name}.json", "w") as worldJSON:
                                worldJSON.write(
                                    session.get(
                                        f"https://lj44.ch/creator/kart/worlds/{worldsInfo[name]['id']}/fabric"
                                    ).text
                                )
                            updateWorlds_output.text += "done!\n"
                            data["version"] = worldsInfo[name]["version"]
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
                                session.get(
                                    f"https://lj44.ch/creator/kart/worlds/{worldsInfo[name]['id']}/fabric"
                                ).text
                            )
                        updateWorlds_output.text += "done!\n"
            finally:
                f.close()

            with open("client/worlds.json", "w") as f:
                json.dump(worldsInfo, f)

            worlds_spinner.values = [world[:-5] for world in listdir("client/worlds")]
            updateWorlds_output.text += "All worlds are up to date!"
            self._updating = False
            self.text = "Update the worlds now"
            if App.get_running_app().soundEnabled:
                sound = SoundLoader.load("client/sounds/success-sound-effect.mp3")
                sound.volume = 0.5
                sound.play()


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


class Controls(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class JoinGame(FloatLayout):
    def join(self):
        pass