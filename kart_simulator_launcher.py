from os import path
import time
import os.path
from typing import List

from kivy.properties import Clock

import client
import game

#########################################################################
######################  App de lancement de kivy  #######################

from kivy.app import App
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


    def updateObstacle(self, obstacleID = None, obstacle = None, relativeMouvement: List[float] = None, absolutePosition: List[float] = None):

        if obstacleID or obstacleID == 0:
            obs = self.dict_objects.get(obstacleID)
            io_obs = self.instanciateObstacle(obs)
        elif obstacle:
            obs = obstacle
            io_obs = self.instanciateObstacle(obs)

        

        if relativeMouvement:
            new_pos_x = relativeMouvement[0]+obs.center().get_x()
            new_pos_y = relativeMouvement[1]+obs.center().get_x()
            new_pos = list(new_pos_x,new_pos_y)
            io_obs.updatePosition(new_pos)

        elif absolutePosition:
            new_pos = absolutePosition
            io_obs.updatePosition(new_pos)

        


    def instanciateObstacle(self, obstacle = None):
        if obstacle:
            if type(obstacle).__name__ == "Circle" and obstacle.formID() not in self.dict_circles:
                # with self.canvas.before:
                io_obstacle = IO_Circle(diametre = 2*obstacle.radius(), position=[obstacle.center()[0],obstacle.center()[1]])
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
        self.manager = self.canvas
        return self.manager

#########################################################################

dataUrl = path.join("client", "circle.json")
print(f"GameData: {dataUrl}")
eventsList = list()

from game.objects import Circle,Object
from lib.point import Point

def output(objects: List[game.objects.Object]):
    for object in objects:
        aa.updateObstacle(obstacle = object)
        # print("object detected")
        cercle_test = Circle()
        cercle_test._radius = 100
        cercle_test._center = Point(100,100)
        cercle_test._formID = 1
    # aa.updateObstacle(obstacle = cercle_test)


theGame = game.Game(dataUrl, eventsList, output)

print("Starting ...")
aa = MainWidget()
bb = MenuApp(aa)
bb.run()

print("Finisched!")
