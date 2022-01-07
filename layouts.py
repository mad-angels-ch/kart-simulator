from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
from kivy.uix.label import Label
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
        self.musicName = self.get_musicName(music)
        self.startMusic()
        super().__init__(**kw)
        self.world = world
        self.game = MainWidget(self.world,self)
        self.layout_id.add_widget(self.game)
        
    def quit(self):
        self.game.clear()
        
    def pauseMode(self):
        if self.musicName:
            self.pauseMusic()
        
        self.game.play = False
        self.game.my_clock.unschedule(self.game.theGame.nextFrame)
        self.pauseMenu = PauseMode(width=Window.width, height = Window.height, music=self.musicName)
        self.add_widget(self.pauseMenu)
        
        
    def resumeGame(self, new_music):
        self.resumeMusic()
        
        self.game.play = True
        self.game.my_clock.schedule_interval(self.game.theGame.nextFrame, 1 / self.game.fps)
        self.remove_widget(self.pauseMenu)
        
    def startMusic(self):
        #Initialization of the music (with repetitions)
        
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

    def changeMusic(self,new_music):
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
        if isinstance(music,StringProperty):
            return music.defaultvalue
        else:
            return music
        





    
    
from kart_simulator import game, path, Rectangle, Color
from os import path, listdir
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
        
    def changeWorldSpinnerText(self, text):
        self.chosen_world = text
    
    def changeMusicSpinnerText(self,text):
        self.chosen_music = text
        
    def generateWorldsList(self):
        return list(world[:-5] for world in listdir("client/worlds"))
    
    def generateMusicsList(self):
        music_list = list(music[:-4] for music in listdir("client/sounds/music"))
        music_list.append("No music")
        return music_list
    

            
            






##########################################################################