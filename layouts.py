from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.utils import rgba
from kart_simulator import MainWidget, PauseMode
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.dropdown import DropDown
from action_bar import BoxLayoutWithActionBar

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
    
    def __init__(self, world, music, **kw):
        #Initialization of the music (with repetitions)
        self.musicPath = path.join("client/sounds/music", music) + ".wav"
        self.music = SoundLoader.load(self.musicPath)
        # self.music_pos = 0
        self.music.volume = 0.05
        self.startMusic()
        
        super().__init__(**kw)
        self.world = world
        self.game = MainWidget(self.world)
        self.layout_id.add_widget(self.game)
        
    def quit(self):
        self.game.clear()
    
    def pauseMode(self):
        self.pauseMusic()
        
        self.game.play = False
        self.game.my_clock.unschedule(self.game.theGame.nextFrame)
        self.pauseMenu = PauseMode(width=Window.width, height = Window.height)
        self.add_widget(self.pauseMenu)
        
        
    def resumeGame(self):
        self.resumeMusic()
        
        self.game.play = True
        self.game.my_clock.schedule_interval(self.game.theGame.nextFrame, 1 / self.game.fps)
        self.remove_widget(self.pauseMenu)
        
    def startMusic(self):
        self.music.play()
        # self.music.seek(self.music_pos)
        self.music.loop = True
    
    def pauseMusic(self):
        # self.music_pos = self.music.get_pos()     #Bug in the kivy sounds class, doesn't work yet...
        self.music.stop()
        self.music.loop = False
        
    def resumeMusic(self):
        self.startMusic()








class KS(BoxLayout):
    
    def __init__(self,world=None, **kwargs):
        super().__init__(**kwargs)
        self.aa = MainWidget()
        self.add_widget(self.aa)
        self.world = StringProperty(world)

    button_text = StringProperty("Pause")
    
    
from kart_simulator import game, path, Rectangle, Color
from os import path, listdir
from posixpath import abspath
from re import S
import time
import os.path
from typing import List

from kivy.core.window import Window


from lib import Point
# from client.worlds import *
import client.worlds
from game.objects import *
import game

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

    def changePreView(self, world):
        if not isinstance(world,StringProperty):
            self.canvas.before.clear()
            self.canvas.clear()
            self.canvas.after.clear()
            print("PREVIEW CLEARED")
            with self.canvas.before:
                Color(rgba=(1,1,1,1))
                Rectangle(pos=(0,0), size=(200,200))
            self.dataUrl = self.dataUrl = path.join("client/worlds", world) + ".json"
            self.theGame = game.Game(self.dataUrl, [], self.instanciateObstacle)
            self.theGame.callOutput()


    def instanciateObstacle(self, objects: List[game.objects.Object]):
        for obstacle in objects:
            if (
                isinstance(obstacle,Circle)
            ):
                # with self.canvas.before:
                self.color = get_color_from_hex(obstacle._fill)
                pos_x = (obstacle.center()[0] - obstacle.radius())/3
                pos_y = (obstacle.center()[1] - obstacle.radius())/3
                with self.canvas.after:
                    Color(rgba=self.color)
                
                    IO_Circle(
                        diametre=2 * obstacle.radius()/3,
                        position=[pos_x, pos_y],
                        couleur=obstacle._fill,
                    
                    )
                    

            elif (
                isinstance(obstacle,Polygon)
            ):
                self.color = get_color_from_hex(obstacle._fill)
                with self.canvas:
                    Color(rgba=self.color)
                    IO_Polygon(
                        summits=obstacle.vertices(), couleur=obstacle._fill, scale = 3
                    )


class MainMenu2(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chosen_world = StringProperty("Choose your world")
        self.chosen_music = StringProperty("Choose your music")
        self.worlds_list=self.generateWorldsList()
        self.music_list = self.generateMusicList()
        
    def changeWorldSpinnerText(self, text):
        self.chosen_world = text
    
    def changeMusicSpinnerText(self,text):
        self.chosen_music = text
        
    def generateWorldsList(self):
        return list(world[:-5] for world in listdir("client/worlds"))
    
    def generateMusicList(self):
        return list(music[:-4] for music in listdir("client/sounds/music"))
            





##########################################################################