
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
    def __init__(self, world, **kw):
        super().__init__(**kw)
        self.world = world
        self.game = MainWidget(self.world)
        self.layout_id.add_widget(self.game)
        test="test"
    def quit(self):
        self.game.clear()
    
    def pauseMode(self):
        # self.manager.push("pauseMenu")
        self.pauseMenu = PauseMode(width=Window.width, height = Window.height)
        self.add_widget(self.pauseMenu)
    def resumeGame(self):
        self.remove_widget(self.pauseMenu)
        self.game.resume()
        




class KS(BoxLayout):
    
    def __init__(self,world=None, **kwargs):
        super().__init__(**kwargs)
        self.aa = MainWidget()
        self.add_widget(self.aa)
        self.world = StringProperty(world)
    def pause(self, button=None):
        if self.button_text == "Pause":
            self.button_text = "Resume"
            self.aa.pause()
        elif self.button_text == "Resume":
            self.button_text = "Pause"
            self.aa.resume()

    button_text = StringProperty("Pause")
    
    
from kart_simulator import game, path, Rectangle, Color
from os import path
from posixpath import abspath
from re import S
import time
import os.path
from typing import List

from kivy.core.window import Window


from lib import Point
import client
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
    from user_actions import (
        keyboard_closed,
        on_keyboard_down,
        on_touch_up,
        on_keyboard_up,
        on_touch_down,
        )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.world = "fabric.json"
            
        ##################### Création de la partie #####################
        self.dataUrl = path.join("client", self.world)
        print(f"GameData: {self.dataUrl}")
        self.eventsList = list()

        from game.objects import Circle, Object
        from lib import Point

        self.theGame = game.Game(self.dataUrl, self.eventsList, self.output)
        print("Starting ...")

        print("Finisched!")
        #################################################################
        
        self.theGame.callOutput()
        with self.canvas:
            Color(rgba=(1,1,1,1))
            Rectangle(pos=(0,0), size=(200,200))

    def changePreView(self, world):
        print("CLEARED")
        self.canvas.clear()
        self.canvas.after.clear()
        with self.canvas:
            Color(rgba=(1,1,1,1))
            Rectangle(pos=(0,0), size=(200,200))
        self.dataUrl = self.dataUrl = path.join("client", world)
        self.theGame = game.Game(self.dataUrl, self.eventsList, self.output)
        self.theGame.callOutput()
        

    def output(self, objects: List[game.objects.Object]):
        for object in objects:
            self.updateObstacle(obstacle=object)

    def updateObstacle(self, obstacleID=None, obstacle=None):
        if obstacleID or obstacleID == 0:
            obs = self.dict_polygons.get(obstacleID)
            

        elif obstacle:
            obs = obstacle
        self.instanciateObstacle(obs)


    def instanciateObstacle(self, obstacle=None):
        if obstacle:
            if (
                isinstance(obstacle,Circle)
                and obstacle.formID()
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
                and obstacle.formID()
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
        self.chosen_world = StringProperty("Chose your world")
    def changeText(self,text):
        self.chosen_world = text
    # def preView(self):
    #     print("previewed")
    #     preView()





##########################################################################