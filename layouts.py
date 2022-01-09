from logging import warning
from kivy.clock import Clock
import requests, json, os, threading

from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.utils import rgba
from game.objects.ObjectFactory import ObjectCountError
from io_objects.io_FilledQuadrilateral import IO_FilledQuadrilateral
from io_objects.io_FinishLine import IO_FinishLine
from io_objects.io_Gate import IO_Gates
from kart_simulator import EndGameMode, MainWidget, PauseMode, BeginningImage
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.core.audio import SoundLoader
from kivy.uix.dropdown import DropDown
from action_bar import BoxLayoutWithActionBar
from game.objects.fill.Hex import Hex
from game.objects.fill.Pattern import Pattern
from kivy.uix.image import Image
#################### Gestion des différents screens ###################


class NavigationScreenManager(ScreenManager):
    screen_stack = []

    def push(self, screen_name):
        if screen_name not in self.screen_stack:
            self.screen_stack.append(self.current)
            self.transition.direction = "left"
            self.current = screen_name

    def pop(self):
        if len(self.screen_stack) > 0:
            screen_name = self.screen_stack[-1]
            del self.screen_stack[-1]
            self.transition.direction = "right"
            self.current = screen_name


class MyScreenManager(NavigationScreenManager):
    pass


class KS_screen(Screen):
    layout_id = ObjectProperty()
    # animation_id = ObjectProperty()
    # imageB = ObjectProperty()

    def __init__(self, world, music, **kw):
        self.musicName = self.get_musicName(music)
        self.startMusic()
        super().__init__(**kw)
        self.world = world
        self.game = MainWidget(self.world, self)
        self.layout_id.add_widget(self.game)
        self.start_button = Button(text="start The game!", size_hint=(.25,.1 ))
        self.start_button.bind(on_press=self.startingAnimation)
        self.layout_id.add_widget(self.start_button)
        self.app = App.get_running_app()
        
    def quit(self):
        self.game.clear()

    def pauseMode(self):
        if self.musicName:
            self.pauseMusic()

        self.game.play = False
        self.game.my_clock.unschedule(self.game.theGame.nextFrame)
        self.pauseMenu = PauseMode(
            width=Window.width, height=Window.height, music=self.musicName
        )
        self.add_widget(self.pauseMenu)
        
    def endGameMode(self):
        if self.musicName:
            self.pauseMusic()

        self.game.play = False
        self.game.my_clock.unschedule(self.game.theGame.nextFrame)
        self.endGameMenu = EndGameMode()
        self.add_widget(self.endGameMenu)
        
    def begin_game(self,dt):
        # self.animation_id.remove_widget(self.imageB)
        # self.remove_widget(self.animation_id)
        self.remove_widget(self.pg)
        
        self.game.start_theGame()
        
    def startingAnimation(self, instance):
        self.layout_id.remove_widget(self.start_button)
        self.pg = BeginningImage()
        self.add_widget(self.pg)
        # self.image3 = Image(source='client/Images/321go.gif', size_hint=(1,1 ),pos_hint={'center_x': .35, 'center_y': .35}, keep_ratio= False,allow_stretch= True)
        # self.layout_id.add_widget(self.image3)
        Clock.schedule_once(self.begin_game, 3)

    def end_game(self):
        self.endGameMode()
        
    def test(self):
        self.app.manager.pop()
        
    def resumeGame(self, new_music):
        self.resumeMusic()

        self.game.play = True
        self.game.my_clock.schedule_interval(
            self.game.theGame.nextFrame, 1 / self.game.fps
        )
        self.remove_widget(self.pauseMenu)

    def startMusic(self):
        # Initialization of the music (with repetitions)

        # if self.music != "No music" and not isinstance(self.music,StringProperty) and self.music.name != "":
        try:
            musicPath = path.join("client/sounds/music", self.musicName) + ".wav"
            self.music = SoundLoader.load(musicPath)
            # self.music_pos = 0
            self.music.volume = 0.25
            self.music.play()
            # self.music.seek(self.music_pos)
            self.music.loop = True

        except:
            pass

    def changeMusic(self, new_music):
        self.musicName = new_music

    def pauseMusic(self):
        try:
            # self.music_pos = self.music.get_pos()     #Bug in the kivy sounds class, doesn't work yet...
            self.music.stop()
            self.music.loop = False
        except:
            pass

    def resumeMusic(self):
        print("ok")
        self.startMusic()

    def get_musicName(self, music):
        if isinstance(music, StringProperty):
            return music.defaultvalue
        else:
            return music


from kart_simulator import game, path, Rectangle, Color
from os import path, listdir, write
from posixpath import abspath
from re import S
import time
import os.path
from typing import List

from kivy.core.window import Window


from lib import Point
import client.worlds
from game.objects import *
import game
from kivy.app import App
from io_objects.io_polygon import IO_Polygon
from io_objects.io_circle import IO_Circle

from kivy.utils import get_color_from_hex, rgba
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.properties import Clock
from kivy.properties import StringProperty


class PreView(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.previewMode = False

    def changePreView(self, world):
        if not isinstance(world, StringProperty):
            self.canvas.before.clear()
            self.canvas.clear()
            self.canvas.after.clear()
            print("PREVIEW CLEARED")
            if self.previewMode:
                try:
                    
                    
                    self.dataUrl = self.dataUrl = (
                        path.join("client/worlds", world) + ".json"
                    )
                    app = App.get_running_app()
                    self.theGame = game.Game(self.dataUrl, [], self.instanciateObstacle)
                    with self.canvas.before:
                        Color(rgba=(1, 1, 1, 1))
                        Rectangle(pos=(0, 0), size=(200, 200))
                    self.theGame.callOutput()
                except ObjectCountError as OCE:
                    app.changeLabelText(OCE.message())
                

    def updatePreviewMode(self):
        self.previewMode = not self.previewMode

    # def instanciateObstacle(self, objects: List[game.objects.Object]):
    #     for obstacle in objects:
    #         if isinstance(obstacle, Circle):
    #             # with self.canvas.before:
    #             self.color = get_color_from_hex(obstacle.fill().value())
    #             pos_x = (obstacle.center()[0] - obstacle.radius()) / 3
    #             pos_y = (obstacle.center()[1] - obstacle.radius()) / 3
    #             with self.canvas.after:
    #                 Color(rgba=self.color)

    #                 IO_Circle(
    #                     diametre=2 * obstacle.radius() / 3,
    #                     position=[pos_x, pos_y],
    #                     couleur=obstacle.fill().value(),
    #                 )

    #         elif isinstance(obstacle, Polygon):
    #             self.color = get_color_from_hex(obstacle.fill().value())
    #             with self.canvas:
    #                 Color(rgba=self.color)
    #                 IO_Polygon(
    #                     summits=obstacle.vertices(),
    #                     couleur=obstacle.fill().value(),
    #                     scale=3,
    #                 )
    def instanciateObstacle(self, objects=None):
        for obstacle in objects:
            print("oui")
            if isinstance(obstacle.fill(), Hex):

                if obstacle:
                    self.color = get_color_from_hex(obstacle.fill().value())

                    if (
                        isinstance(obstacle, Circle)
                    ):
                        with self.canvas:
                            Color(rgba=self.color)
                        pos_x = obstacle.center()[0] - obstacle.radius()
                        pos_y = obstacle.center()[1] - obstacle.radius()
                        io_obstacle = IO_Circle(
                            diametre=2 * obstacle.radius(),
                            position=[pos_x, pos_y],
                            couleur=obstacle.fill().value(),
                            scale=3
                        )
                        self.canvas.add(io_obstacle)

                    # elif isinstance(obstacle, Circle):
                    #     io_obstacle = self.dict_circles.get(obstacle.formID())

                    elif (
                        isinstance(obstacle, Polygon)
                    ):
                        print(obstacle.formID())
                        if type(obstacle).__name__ == "Kart":
                            self.kart_ID = obstacle.formID()
                            with self.canvas:
                                Color(rgba=(1,1,1,1))
                                io_obstacle = IO_FilledQuadrilateral(height=16,width=50,center=obstacle.center(), source="client/Images/kartInGame.jpg", angle=obstacle.angle(), scale=3)
                                
                        else:
                            with self.canvas:
                                Color(rgba=self.color)
                            io_obstacle = IO_Polygon(
                                summits=obstacle.vertices(), couleur=obstacle.fill().value(), scale=3
                            )
                            self.canvas.add(io_obstacle)

                    # elif isinstance(obstacle, Polygon):
                    #     io_obstacle = self.dict_polygons.get(obstacle.formID())
                    # return io_obstacle

            elif isinstance(obstacle.fill(), Pattern):
                if len(obstacle) == 4:
                    if type(obstacle).__name__ == "Gate":
                        with self.canvas:
                            io_obstacle = IO_Gates(
                                summitsBeforeRotation=obstacle.verticesBeforeRotation(),
                                angle=obstacle.angle(),
                                scale=3
                            )
                    elif type(obstacle).__name__ == "FinishLine":
                        with self.canvas:
                            io_obstacle = IO_FinishLine(
                                summitsBeforeRotation=obstacle.verticesBeforeRotation(),
                                angle=obstacle.angle(),
                                scale=3
                            )
                    else:
                        warning("TO BE IMPLEMENTED")
                        source = obstacle.sourceImage
                        with self.canvas:
                            io_obstacle = IO_FilledQuadrilateral(
                                summitsBeforeRotation=obstacle.verticesBeforeRotation(),
                                source=source,
                                angle=obstacle.angle(),
                                scale=3
                            )
                else:
                    raise "Only quadrilaterals can be filled with a pattern"


            else:
                raise "Unsupported color type"

class MainMenu2(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chosen_world = StringProperty("Choose your world")
        self.chosen_music = StringProperty("Choose your music")

    def changeWorldSpinnerText(self, text):
        self.chosen_world = text

    def changeMusicSpinnerText(self, text):
        self.chosen_music = text

    def generateWorldsList(self):
        return [world[:-5] for world in listdir("client/worlds")]

    def generateMusicsList(self):
        music_list = list(music[:-4] for music in listdir("client/sounds/music"))
        music_list.append("No music")
        return music_list


class UpdateWorldButton(Button):
    def __init__(self, **kwargs):
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
        updateWorlds_output.text = (
            "\nUpdating the worlds (this may take several minutes) ...\n"
        )
        worldsInfo = {}
        for world in requests.get(
            "https://lj44.ch/creator/kart/worldsjson",
            {"id": True, "version": True, "name": True},
        ).json():
            worldsInfo[world["name"]] = {"id": world["id"], "version": world["version"]}
        with open("client/worlds.json", "r") as f:
            savedWorld = json.load(f)
            # mise à jour des mondes déjà téléchargés
            for name, data in savedWorld.items():
                if name in worldsInfo:
                    if data["version"] != worldsInfo[name]["version"]:
                        updateWorlds_output.text += f"Updating world {name} ..."
                        with open(f"client/worlds/{name}.json", "w") as worldJSON:
                            worldJSON.write(
                                requests.get(
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
                            requests.get(
                                f"https://lj44.ch/creator/kart/worlds/{worldsInfo[name]['id']}/fabric"
                            ).text
                        )
                    updateWorlds_output.text += "done!\n"

        with open("client/worlds.json", "w") as f:
            json.dump(worldsInfo, f)

        worlds_spinner.values = [world[:-5] for world in listdir("client/worlds")]
        updateWorlds_output.text += "All worlds are up to date!"
        self._updating = False
        self.text = "Update the worlds now (this may take several minutes)"
        sound = SoundLoader.load('client/sounds/success-sound-effect.mp3')
        sound.volume = 0.25
        sound.play()


##########################################################################
