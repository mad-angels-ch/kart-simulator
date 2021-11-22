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



class preView(Widget):
    from user_actions import (
    keyboard_closed,
    on_keyboard_down,
    on_touch_up,
    on_keyboard_up,
    on_touch_down,
    )
    dict_polygons = dict()
    dict_circles = dict()
    
    def __init__(self,world="2triangles.json", **kwargs):
        super().__init__(**kwargs)
        
        self.world = world
        if isinstance(self.world,StringProperty):
            self.world = "2triangles.json"
            
        ##################### Création de la partie #####################
        dataUrl = path.join("client/worlds", self.world)
        print(f"GameData: {dataUrl}")
        self.eventsList = list()

        from game.objects import Circle, Object
        from lib import Point

        self.theGame = game.Game(dataUrl, self.eventsList, self.output)
        print("Starting ...")

        print("Finisched!")
        #################################################################


    def changePreView(self):
        print("LEAVED")
        self.canvas.clear()

    def output(self, objects: List[game.objects.Object]):
        for object in objects:
            self.updateObstacle(obstacle=object)

    def updateObstacle(self, obstacleID=None, obstacle=None):
        if obstacleID or obstacleID == 0:
            obs = self.dict_polygons.get(obstacleID)
            io_obs = self.instanciateObstacle(obs)

        elif obstacle:
            obs = obstacle
            io_obs = self.instanciateObstacle(obs)


    def instanciateObstacle(self, obstacle=None):
        if obstacle:
            if (
                isinstance(obstacle,Circle)
                and obstacle.formID() not in self.dict_circles
            ):
                # with self.canvas.before:
                self.color = get_color_from_hex(obstacle._fill)
                with self.canvas:
                    Color(rgba=self.color)
                pos_x = (obstacle.center()[0] - obstacle.radius())/10
                pos_y = (obstacle.center()[1] - obstacle.radius())/10
                io_obstacle = IO_Circle(
                    diametre=2 * obstacle.radius()/10,
                    position=[pos_x, pos_y],
                    couleur=obstacle._fill,
                )
                self.canvas.add(io_obstacle)
                self.dict_circles[obstacle.formID()] = io_obstacle


            elif (
                isinstance(obstacle,Polygon)
                and obstacle.formID() not in self.dict_polygons
            ):
                self.color = get_color_from_hex(obstacle._fill)
                with self.canvas:
                    Color(rgba=self.color)
                io_obstacle = IO_Polygon(
                    summits=obstacle.vertices(), couleur=obstacle._fill
                )
                self.canvas.add(io_obstacle)
                self.dict_polygons[obstacle.formID()] = io_obstacle


