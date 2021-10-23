from os import path
from re import S
import time
import os.path
from typing import List

from kivy.properties import Clock
from kivy.utils import get_color_from_hex, rgba

import client
import game

#########################################################################
######################  App de lancement de kivy  #######################

from kivy.app import App
from game.objects.motions.angulars.AngularMotion import AngularMotion
from navigation_screen_manager import ObjectProperty, MyScreenManager


from kivy.context import register_context
from kivy.core import window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.properties import Clock
from kivy.core.window import Window

from io_objects.io_polygon import IO_Polygon
from io_objects.io_circle import IO_Circle
from io_objects.kart import Kart


from kivy.graphics.context_instructions import PushMatrix, PopMatrix, Rotate, Translate, Scale, MatrixInstruction

Builder.load_file("layouts.kv")


class MainWidget(Widget):


    dict_objects = dict()
    dict_circles = dict()

    vertices = list()
    indices = list()
    step = int()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        
        Clock.schedule_interval(theGame.nextFrame,1/60)


    def updateObstacle(self, dt = 0, obstacleID = None, obstacle = None, relativeMouvement: List[float] = None, absolutePosition: List[float] = None):

        if obstacleID or obstacleID == 0:
            obs = self.dict_objects.get(obstacleID)
            io_obs = self.instanciateObstacle(obs)
            
        elif obstacle:
            obs = obstacle
            io_obs = self.instanciateObstacle(obs)


        if relativeMouvement:
            new_pos_x = relativeMouvement[0]+obs.center().get_x()
            new_pos_y = relativeMouvement[1]+obs.center().get_y()
            new_pos = [new_pos_x,new_pos_y]

        elif absolutePosition:
            new_pos = absolutePosition

        else:
            new_pos_x = obs.center().get_x()
            new_pos_y = obs.center().get_y()
            new_pos = [new_pos_x,new_pos_y]

        io_obs.updatePosition(newPos=new_pos)

        if obs._fill != io_obs.color:
            self.canvas.remove(io_obs)
            if type(obs).__name__ == "Circle":
                self.dict_circles.pop(obs.formID())
                self.color = get_color_from_hex(obs._fill)
                with self.canvas:
                    Color(rgba=self.color)
                io_obs = IO_Circle(diametre = 2*obs.radius(), position=[obs.center()[0],obs.center()[1]], couleur=obs._fill)
                self.canvas.add(io_obs)
                self.dict_circles[obs.formID()] = io_obs



    def instanciateObstacle(self, obstacle = None):
        if obstacle:
            if type(obstacle).__name__ == "Circle" and obstacle.formID() not in self.dict_circles:
                # with self.canvas.before:
                self.color = get_color_from_hex(obstacle._fill)
                with self.canvas:
                    Color(rgba=self.color)
                io_obstacle = IO_Circle(diametre = 2*obstacle.radius(), position=[obstacle.center()[0],obstacle.center()[1]], couleur=obstacle._fill)
                self.canvas.add(io_obstacle)
                self.dict_circles[obstacle.formID()] = io_obstacle
            else:
                io_obstacle = self.dict_circles.get(obstacle.formID())

            # elif type(obstacle).__name__ == "Polygon" and obstacle.formID() not in self.dict_objects:
                # with self.canvas.before:
                #     io_obstacle = IO_Polygon() #A compléter !!!!!!!!!!!!!!!!!!!!!!!!!!!!
                #     pass
                # self.dict_objects[obstacle.formID()] = io_obstacle

        return io_obstacle

class MenuApp(App):
    manager = ObjectProperty(None)
    def __init__(self,canvas,**kwargs):
        super().__init__(**kwargs)
        self.canvas = canvas
    def build(self):
        Window.clearcolor=get_color_from_hex('#ffffff')
        self.manager = self.canvas
        return self.manager

#########################################################################

if __name__ == "__main__":
    dataUrl = path.join("client", "circle.json")
    print(f"GameData: {dataUrl}")
    eventsList = list()

    from game.objects import Circle,Object
    from lib.point import Point

    def output(elapsedTime, objects: List[game.objects.Object]):
        for object in objects:
            aa.updateObstacle(dt = elapsedTime, obstacle = object)


    theGame = game.Game(dataUrl, eventsList, output)

    print("Starting ...")
    aa = MainWidget()
    bb = MenuApp(aa)
    bb.run()

    print("Finisched!")
