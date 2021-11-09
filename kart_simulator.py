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



Builder.load_file("layouts.kv")



class MainWidget(Widget):
    from user_actions import (
    keyboard_closed,
    on_keyboard_down,
    on_touch_up,
    on_keyboard_up,
    on_touch_down,
    )
    dict_polygons = dict()
    dict_circles = dict()

    vertices = list()
    indices = list()
    step = int()
    
    def __init__(self,world="2triangles.json", **kwargs):
        super().__init__(**kwargs)
        self.world = world
        ##################### Création de la partie #####################
        dataUrl = path.join("client", self.world)
        print(f"GameData: {dataUrl}")
        self.eventsList = list()

        from game.objects import Circle, Object
        from lib import Point

        self.theGame = game.Game(dataUrl, self.eventsList, self.output)
        print("Starting ...")

        print("Finisched!")
        #################################################################

        self.fps = 60


        self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_keyboard_down)
        self._keyboard.bind(on_key_up=self.on_keyboard_up)

        self.my_clock = Clock
        self.my_clock.schedule_interval(self.theGame.nextFrame, 1 / self.fps)

    def clear(self):
        print("LEAVED")
        self.canvas.clear()
        self.pause()

    def pause(self):
        self.my_clock.unschedule(self.theGame.nextFrame)

    def resume(self):
        self.my_clock.schedule_interval(self.theGame.nextFrame, 1 / self.fps)

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

        if isinstance(obs,Circle):
            new_pos = obs.center()

        elif isinstance(obs,Polygon):
            new_pos = obs.vertices()

        io_obs.updatePosition(newPos=new_pos)

        if (
            obs._fill != io_obs.color
        ):  # En cas de changement de couleur de l'obstacle, kivy nous oblige à le redessiner
            self.canvas.remove(io_obs)
            if isinstance(obs,Circle):
                self.dict_circles.pop(obs.formID())
            elif isinstance(obs,Polygon):
                self.dict_polygons.pop(obs.formID())
                
            self.instanciateObstacle(obstacle=obs)



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
                pos_x = obstacle.center()[0] - obstacle.radius()
                pos_y = obstacle.center()[1] - obstacle.radius()
                io_obstacle = IO_Circle(
                    diametre=2 * obstacle.radius(),
                    position=[pos_x, pos_y],
                    couleur=obstacle._fill,
                )
                self.canvas.add(io_obstacle)
                self.dict_circles[obstacle.formID()] = io_obstacle

            elif isinstance(obstacle,Circle):
                io_obstacle = self.dict_circles.get(obstacle.formID())

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

            elif isinstance(obstacle,Polygon):
                io_obstacle = self.dict_polygons.get(obstacle.formID())
            return io_obstacle

