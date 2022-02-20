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
from game.objects import Circle, Object
from lib import Point


Builder.load_file("layouts.kv")


class MainWidget(Widget):
    from user_actions import (
        keyboard_closed,
        on_keyboard_down,
        on_keyboard_up
    )

    dict_polygons = dict()
    dict_circles = dict()
    dict_gates = dict()
    dict_finishLines = dict()
    dict_FilledQuadrilaterals = dict()
    kart_ID = 0

    def __init__(self, world=None, parentScreen=None, POV = "Third Person", **kwargs):
        """Canvas dans lequel les objets d'une partie sont dessinés"""
        super().__init__(**kwargs)
        self.world = world
        self.POV = POV
        self.parentScreen = parentScreen
        self.play = -1
        if isinstance(self.world, StringProperty):
            self.world = "2triangles"

        ##################### Création de la partie #####################
        if self.world != "client/easteregg.json":
            dataUrl = path.join("client/worlds", self.world) + ".json"
            self.isEasterEgg = False
        else:
            dataUrl = self.world
            self.isEasterEgg = True
        self.eventsList = list()
        # Récupération de l'app principale
        self.app = App.get_running_app()
        # A condition que ObjectFactory n'ai pas renvoyé d'erreur lorsde la création des objets physiques
        with open(dataUrl, "r", encoding="utf8") as f:
            try:
                # Création de la partie
                self.theGame = game.Game(
                    f.read(),
                    OutputFactory(
                        self,
                        frame_callback=self.frame_callback,
                        max_width=self.app.windowSize[0],
                        max_height=self.app.windowSize[1],
                        POV = self.POV
                    ),
                )

                self.app.manager.add_widget(self.parentScreen)
                self.app.start_ks()
                #################################################################
                self.fps = 60

            except ObjectCountError as OCE:
                self.theGame = None
                self.app.changeLabelText(OCE.message())

    def nextFrame(self, elapsedTime: float) -> None:
        self.theGame.nextFrame(elapsedTime, self.eventsList)
        self.eventsList.clear()

    def clear(self) -> None:
        """Nettoyage du canvas de jeu et arrêt de la pendule"""
        self.canvas.clear()
        if self.play == 1:
            self.my_clock.unschedule(self.nextFrame)

    def change_gameState(self) -> None:
        """Change l'état du jeu: pause ou jeu"""
        if self.play == 1:
            self.parent.parent.pauseMode()
        else:
            self.parent.parent.resumeGame()

    def start_theGame(self) -> None:
        """Instantation du clavier, des commandes liées et de la pendule"""
        self.timer = 0
        self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_keyboard_down)
        self._keyboard.bind(on_key_up=self.on_keyboard_up)
        self.my_clock = Clock
        self.my_clock.schedule_interval(self.nextFrame, 1 / self.fps)

        self.play = 1

    def frame_callback(self, output: OutputFactory, objects: List[Object]) -> None:
        """Fonction appellée à chaque frame par output"""
        if output.isInitialized() and not self.isEasterEgg:
            self.updateGatesCount(output.getAllGates())
            self.updateLapsCount(output.getFinishLine())
            self.updateTimer()
            self.checkIfGameIsOver(output.getAllKarts(), output.getFinishLine())
            
    def updateTimer(self) -> None:
        """Mise à jour du timer"""
        self.timer += 1/self.fps
        s, mili = divmod(int(1000*self.timer), 1000)
        min, s= divmod(s, 60)
        if mili > 100:
            self.parent.parent.parent.ids.timer_id.text = (f'{min:d}:{s:02d}:{mili:02d}')
        else:
            self.parent.parent.parent.ids.timer_id.text = (f'{min:d}:{s:02d}:0{mili:02d}')
    
    def updateLapsCount(self, finishLine: FinishLine) -> None:
        """Met l'affichage du nombre de tours terminés à jour"""
        self.parent.parent.parent.ids.laps_id.text = f"{finishLine.passagesCount(self.kart_ID)}/{finishLine.numberOfLapsRequired()}"

    def updateGatesCount(self, gatesList: List[Gate]) -> None:
        """Met l'affiche du nombre de portillons (du tour) franchis à jour"""
        numberOfGates = len(gatesList)
        gatesPassed = (
            sum([gate.passagesCount(self.kart_ID) for gate in gatesList])
            % numberOfGates
        )
        self.parent.parent.parent.ids.gates_id.text = f"{gatesPassed}/{numberOfGates}"

    def checkIfGameIsOver(self, karts: List[Kart], finishLine: FinishLine) -> None:
        """Contrôle si la partie est terminée et si oui gère celle-ci"""
        if finishLine.completedAllLaps(self.kart_ID):
            self.parentScreen.end_game(f"Completed!\n\nWell done!\n Your time: {self.parent.parent.parent.ids.timer_id.text}")
        elif karts[0].hasBurned():
            self.parentScreen.end_game("You have burned!\n\nTry again!")
