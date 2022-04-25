import json
from os import path
from threading import Thread
from typing import List

import game
from game.objects import *
from game.objects import Circle, Object
from game.objects.FinishLine import FinishLine
from game.objects.ObjectFactory import InvalidWorld
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import Clock

from .output import OutputFactory


class SingleplayerGame:
    from client.output.solo_user_actions import (  # on_touch_up,; on_touch_down,
        keyboard_closed,
        on_keyboard_down,
        on_keyboard_up,
    )

    kart_ID = 0
    completed_time = None
    burned = False
    completed = False

    def __init__(
        self, world, output, onCollision, changeLabelText, parentScreen, **kwargs
    ):
        """Canvas dans lequel les objets d'une partie en solo sont dessinés"""
        super().__init__(**kwargs)
        self.world = world
        self.parentScreen = parentScreen
        self._output = output
        self._output.set_frameCallback(self.frame_callback)
        ##################### Création de la partie #####################
        if self.world != "client/easteregg.json":
            with open("client/worlds.json", "r", encoding="utf8") as f:
                worlds = json.load(f)
                self.worldVersion_id = worlds[self.world]["version_id"]
            dataUrl = path.join("client/worlds", self.world) + ".json"
            self.isEasterEgg = False
        else:
            dataUrl = self.world
            self.isEasterEgg = True
        self.eventsList = list()

        # Récupération de l'app principale
        self.app = App.get_running_app()
        # A condition que ObjectFactory n'ait pas renvoyé d'erreur lorsde la création des objets physiques

        try:
            with open(dataUrl, "r", encoding="utf8") as f:
                # Création de la partie
                self._game = game.Game(
                    f.read(),
                    self._output,
                )
                self.kart_ID = self._game.loadKart(
                    "Me", self.app.get_userSettings()["kart"]
                )

                self.app.start_ks()
                self.fps = 60

        except InvalidWorld as IW:
            self._game = None
            changeLabelText(IW.message())  # Affichage de l'erreur obtenue
        else:
            factory = self._game.objectsFactory()
            self.parentScreen.updateLapsAndGatesCount(factory, factory[self.kart_ID])
            self.y = 0  # Pour une raison inconnue, lors du redimensionnement d'une fenêtre (qui n'arrive normalement pas car le jeu est par défaut en plein écran), kivy essaie de retrouver la "hauteur" "self.y" de cette classe alors qu'elle n'est en rien liée à l'application graphique... n'ayant pas réussi à régler le problème autrement, nous avons créé la méthode to_window() et l'attribut "y" qui règlent le problème.

    def to_window(self, a, b):
        # c.f. commentaire de self.y ci-dessus
        return self.app.windowSize()

    def nextFrame(self, elapsedTime: float) -> None:
        self._game.nextFrame(elapsedTime, self.eventsList)
        self.eventsList.clear()

    def disconnect(self) -> None:
        """Déconnection du joueur lorsqu'il quitte la partie. Utile uniquement pour le multijoueur."""
        pass

    def finish_game(self) -> None:
        """Arrêt de la pendule"""
        self.my_clock.unschedule(self.nextFrame)
        self.play = False

    def change_gameState(self) -> None:
        """Change l'état du jeu: pause ou jeu"""
        if self.play:
            self.play = False
            self.my_clock.unschedule(self.nextFrame)
            self.parentScreen.pauseMode()
        else:
            self.play = True
            self.my_clock.schedule_interval(self.nextFrame, 1 / self.fps)
            self.parentScreen.resumeGame()
            self._game.unloadKart(placeHolder=self.kart_ID)
            Clock.schedule_once(
                lambda a: self._game.loadKart(
                    placeHolder=self.kart_ID,
                    username="",
                    img=self.app.get_userSettings()["kart"],
                ),
                2 / self.fps,
            )

    def start_theGame(self) -> None:
        """Instantation du clavier, des commandes liées et de la pendule"""
        self.timer = 0
        self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_keyboard_down)
        self._keyboard.bind(on_key_up=self.on_keyboard_up)
        self.my_clock = Clock
        self.my_clock.schedule_interval(self.nextFrame, 1 / self.fps)

        self.play = True

    def frame_callback(self, output: OutputFactory, objects: List[Object]) -> None:
        """Fonction appellée à chaque frame par output"""
        if output.isInitialized() and not self.isEasterEgg:
            factory = self._game.objectsFactory()
            self.parentScreen.updateLapsAndGatesCount(factory, factory[self.kart_ID])
            self.timer += 1 / self.fps
            self.parentScreen.updateTimer(self.timer)
            self.checkIfGameIsOver(output.getAllKarts(), output.getFinishLine())

    def checkIfGameIsOver(self, karts: List[Kart], finishLine: FinishLine) -> None:
        """Contrôle si la partie est terminée et si oui gère celle-ci"""
        if not self.completed:
            if finishLine.completedAllLaps(self.kart_ID):
                self.completed_time = self.timer
                self.completed = True
                self.parentScreen.end_game(
                    f"Completed!\n\nWell done!\n Your time: {self.parentScreen.ids.timer_id.text}"
                )

            elif karts[0].hasBurned() and not self.burned:
                self.parentScreen.end_game("You have burned!\n\nTry again!")
                self.completed_time = self.timer
                self.burned = True

    def save(self) -> None:
        """Sauvegarde la partie sur lj44.ch"""
        if not self.isEasterEgg:
            if self.completed_time == None:
                self.completed_time = self.timer
            Thread(
                target=self.app.session.post,
                args=(
                    self.app.server + "/games/kart/savesologame",
                    {
                        "worldVersion_id": self.worldVersion_id,
                        "duration": self.timer,
                        "movements": "",
                        "finishTime": self.completed_time,
                        "burned": self.burned,
                        "completed": self.completed,
                    },
                ),
            ).start()
