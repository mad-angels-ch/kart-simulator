from os import path
from posixpath import abspath
from re import S
from sys import hexversion
import time
import os.path
from typing import Dict, List
from os import listdir
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from game.objects.FinishLine import FinishLine
from game.objects.ObjectFactory import ObjectCountError
from game.objects.fill.Hex import Hex
from game.objects.fill.Pattern import Pattern
from game import objects
from logging import error, warning
from kivy.app import App
from lib import Point
import client
from game.objects import *
import game
import datetime
from kivy.utils import get_color_from_hex, rgba
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.properties import Clock
from kivy.properties import StringProperty


from client.output import OutputFactory

Builder.load_file("layouts.kv")


class MainWidget(Widget):
    from user_actions import (
        keyboard_closed,
        on_keyboard_down,
        # on_touch_up,
        on_keyboard_up,
        # on_touch_down,
    )

    dict_polygons = dict()
    dict_circles = dict()
    dict_gates = dict()
    dict_finishLines = dict()
    dict_FilledQuadrilaterals = dict()
    kart_ID = 0

    def __init__(self, world=None, parentScreen=None, **kwargs):
        super().__init__(**kwargs)
        self.world = world
        self.parentScreen = parentScreen
        if isinstance(self.world, StringProperty):
            self.world = "2triangles"
        # io_obstacle = IO_FinishLine()
        # self.canvas.add(io_obstacle)

        ##################### Création de la partie #####################
        dataUrl = path.join("client/worlds", self.world) + ".json"
        print(f"GameData: {dataUrl}")
        self.eventsList = list()

        from game.objects import Circle, Object
        from lib import Point

        self.app = App.get_running_app()
        try:
            # self.theGame = game.Game(dataUrl, self.eventsList, self.output)
            self.theGame = game.Game(
                dataUrl,
                self.eventsList,
                OutputFactory(
                    self,
                    frame_callback=self.frame_callback,
                    max_width=self.app.windowSize[0],
                    max_height=self.app.windowSize[1],
                ),
            )

            print("Starting ...")
            self.app.manager.add_widget(self.parentScreen)
            self.app.start_ks()
            print("Finisched!")
            #################################################################
            self.fps = 60

            # self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            # self._keyboard.bind(on_key_down=self.on_keyboard_down)
            # self._keyboard.bind(on_key_up=self.on_keyboard_up)

            # self.my_clock = Clock
            # self.my_clock.schedule_interval(self.theGame.nextFrame, 1 / self.fps)

            # self.play = True

        except ObjectCountError as OCE:
            self.theGame = None
            self.app.changeLabelText(OCE.message())

    def clear(self):
        print("LEAVED")
        self.canvas.clear()
        if self.play:
            self.my_clock.unschedule(self.theGame.nextFrame)

    def change_gameState(self):
        if self.play:
            # self.pause()
            self.parent.parent.pauseMode()
        else:
            # self.resume()
            self.parent.parent.resumeGame()

    def start_theGame(self):
        self.timer = 0
        self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_keyboard_down)
        self._keyboard.bind(on_key_up=self.on_keyboard_up)
        self.my_clock = Clock
        self.my_clock.schedule_interval(self.theGame.nextFrame, 1 / self.fps)

        self.play = True

    def frame_callback(self, output: OutputFactory, objects: List[Object]) -> None:
        """Fonction appellée à chaque frame par output"""
        if output.isInitialized():
            self.updateGatesCount(output.getAllGates())
            self.updateLapsCount(output.getFinishLine())
            self.updateTimer()
            self.checkIfGameIsOver(output.getAllKarts(), output.getFinishLine())
            
    def updateTimer(self) -> None:
        self.timer += 1/self.fps
        s, mili = divmod(int(1000*self.timer), 1000)
        min, s= divmod(s, 60)
        if mili > 100:
            self.parent.parent.ids.timer_id.text = (f'{min:d}:{s:02d}:{mili:02d}')
        # (f'{min:d}:{s:02d}:{mili:02d}')
        else:
            self.parent.parent.ids.timer_id.text = (f'{min:d}:{s:02d}:0{mili:02d}')
    
    def updateLapsCount(self, finishLine: FinishLine) -> None:
        """Met l'affichage du nombre de tours terminés à jour"""
        self.parent.parent.ids.laps_id.text = f"{finishLine.passagesCount(self.kart_ID)}/{finishLine.numberOfLapsRequired()}"

    def updateGatesCount(self, gatesList: List[Gate]) -> None:
        """Met l'affiche du nombre de portillons (du tour) franchis à jour"""
        numberOfGates = len(gatesList)
        gatesPassed = (
            sum([gate.passagesCount(self.kart_ID) for gate in gatesList])
            % numberOfGates
        )
        self.parent.parent.ids.gates_id.text = f"{gatesPassed}/{numberOfGates}"

    def checkIfGameIsOver(self, karts: List[Kart], finishLine: FinishLine) -> None:
        """Control si la partie est terminé et si oui gère celle-ci."""
        if finishLine.completedAllLaps(self.kart_ID):
            self.parentScreen.end_game(f"Completed!\n\nWell done!\n Your time: {self.parent.parent.ids.timer_id.text}")
        elif karts[0].hasBurned():
            self.parentScreen.end_game("You have burned!\n\nTry again!")
