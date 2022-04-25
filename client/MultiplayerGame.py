from typing import Callable, Dict, List, Tuple, AnyStr
import click
import engineio
from socketio import Client, ClientNamespace
from socketio.exceptions import BadNamespaceError
from requests import Session
from client.output.screens.InGameScreen import KS_screen, WaitingRoom

from game import Game, OnCollisionT
from game.objects import Object, Kart, FinishLine, Gate
from game.events import Event, KartMoveEvent, KartTurnEvent
from game.objects.Kart import Kart
import lib
from client.output.outputFactory import OutputFactory

from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window


class MultiplayerGame(ClientNamespace):
    _game: Game
    _sio: Client
    _myKart: "Kart | None" = None
    _lastEvent: "Event | None" = None
    _connectedPlayers: List[str]

    def __init__(
        self,
        session: Session,
        server: str,
        name: str,
        output: OutputFactory,
        changeLabelText: Callable[[AnyStr], None],
        parentScreen: KS_screen,
        onCollision: OnCollisionT = lambda o, p: None,
        worldVersion_id: "int | None" = None,
    ):
        super().__init__("/kartmultiplayer")
        self.play = False
        self.parentScreen = parentScreen
        self._name = name
        self._worldVersion_id = worldVersion_id
        self._changeLabelText = changeLabelText
        output.set_frameCallback(self.frame_callback)
        self._game = Game("", output, onCollision)
        self._sio = Client(http_session=session)
        self.app = App.get_running_app()
        try:
            self._sio.register_namespace(self)
            self._sio.connect(server, namespaces="/kartmultiplayer")
        except:
            self.fatalError(
                error="Couldn't reach the server. Please check your internet connection and try again."
            )
        else:
            self._connectedPlayers = []
            self.app.start_ks()
            self.waitingScreen = WaitingRoom(size_hint=(1, 1))
            self.parentScreen.add_widget(self.waitingScreen)
            self.play = True

        self.y = 0
        # Pour une raison inconnue, lors du redimensionnement d'une fenêtre (qui n'arrive normalement pas car le jeu est par défaut en plein écran),
        # kivy essaie de retrouver la "hauteur" "self.y" de cette classe alors qu'elle n'est en rien liée à l'application graphique...
        # N'ayant pas réussi à régler le problème autrement, nous avons créé la méthode to_window() et l'attribut "y" qui règlent le problème.

    from .output.multi_user_actions import (
        keyboard_closed,
        keyboard_down,
        keyboard_up,
        touch_up,
        touch_down,
    )

    def to_window(self, a, b):
        # c.f. commentaire de self.y ci-dessus
        return self.app.windowSize()

    def change_gameState(self) -> None:
        """Change l'état du jeu: pause ou jeu"""
        if self.play:
            self.play = False
            self.parentScreen.pauseMode()
        else:
            self.play = True
            self.parentScreen.resumeGame()
            if self.myKart():
                self.myKart().set_image(self.app.get_userSettings()["kart"])

    def error(self, error: "None | str" = None) -> None:
        """Gestion des erreurs non fatales"""
        print(error)

    def fatalError(self, error: "None | str" = None) -> None:
        """Gestion des erreurs fatales"""
        if error:
            self._changeLabelText("Fatal error...\n" + error)
            print(error)
            self.disconnect()

    def joiningError(self, error: "None | str" = None) -> None:
        """Gestion des erreur d'entrées en parties"""
        if error:
            print(error)
            if click.confirm("Do you want to try again?"):
                self.emit("join", self._name, callback=self.joiningError)

    def start(self) -> None:
        self.emit("start")
        self.waitingScreen.remove_widget(self.start_button)

    def newEvent(self, event: Event) -> None:
        """Fonction permettant la transmition d'inputs du joueur au server"""
        if event != self._lastEvent:
            self._lastEvent = event
            try:
                self.emit("event", (event.__class__.__name__, event.toTuple()))
            except BadNamespaceError:
                self.error("Couldn't transmit the event to the server")
            except BaseException as e:
                raise e

    def createStartButton(self) -> None:
        self.start_button = Button(
            text="start The game!",
            size_hint=(0.25, 0.1),
            pos_hint={"center_x": 0.5, "y": 0.1},
        )  # Création du bouton qui permet de démarrer la partie
        self.start_button.bind(on_press=lambda _: self.start())
        self.waitingScreen.add_widget(self.start_button)

    def on_connect(self):
        self.executeInMainKivyThread(self.bind_keyboard)
        if self._worldVersion_id == None:
            self.emit("join", self._name, callback=self.joiningError)
        else:
            self.executeInMainKivyThread(self.createStartButton)
            self.emit(
                "create",
                (self._name, self._worldVersion_id),
                callback=self.joiningError,
            )  # Informe le serveur de la création d'une partie
            self._worldVersion_id = None

    def on_countdown(self):
        self.executeInMainKivyThread(
            self.parentScreen.startingAnimation, start_theGame=lambda: None
        )
        self.executeInMainKivyThread(
            self.parentScreen.remove_widget, self.waitingScreen
        )

    def on_passage(self, gate, kart, count) -> None:
        """Evènement appelé à chaque fois qu'un kart passe une gate"""
        self._game.objectByFormID(gate).set_passagesCount(kart, count)

    def on_game_data(self, data: dict):
        """Evènement appelé à chaque nouvelle factory partagée par le serveur.
        Recréé la factory locale en fonction des informations reçues."""
        self.executeInMainKivyThread(self._game.minimalImport, data)
        self.executeInMainKivyThread(self.get_myKart)
        self.executeInMainKivyThread(self.checkIfNewConnection)

    def on_objects_update(self, outputs: Dict[int, Tuple[float, float, float]]):
        """Evènement appelé à chaque nouvelle position d'objets reçus.
        Met la liste des objets à jour en fonction de celles-ci."""
        for formID, newPos in outputs.items():
            formID = int(formID)
            try:
                obj = self._game.objectByFormID(formID)
            except KeyError:
                continue
            obj.set_center(lib.Point(newPos))
            obj.set_angle(newPos[2])
        self.callOutput()
        self.parentScreen.updateLapsAndGatesCount(
            self._game.objectsFactory(), self.myKart()
        )
        self.parentScreen.updateTimer(0)

    def new_connection(self, player: str) -> None:
        self.waitingScreen.add_player(player)

    def new_disconnection(self, player: str) -> None:
        self.waitingScreen.remove_player(player)

    def on_disconnect(self) -> None:
        print("Connection perdue")

    def executeInMainKivyThread(self, function, *args, **kwargs) -> None:
        Clock.schedule_once(lambda _: function(*args, **kwargs), 0)

    def frame_callback(self, output: OutputFactory, objects: List[Object]) -> None:
        pass

    def callOutput(self) -> None:
        self.executeInMainKivyThread(self._game.callOutput)

    def myKart(self) -> Kart:
        """Retourne le kart associé au joueur connecté."""
        return self._myKart

    def get_myKart(self) -> int:
        for kart in self._game.karts():
            if kart.username() == self.app.get_userSettings()["username"]:
                self._myKart = kart  # Récupère le kart associé au joueur connecté.

    def checkIfGameIsOver(self, karts: List[Kart], finishLine: FinishLine) -> None:
        """Contrôle si la partie est terminée et si oui gère celle-ci"""
        # if not self.completed:
        #     if finishLine.completedAllLaps(self.kart_ID):
        #         self.completed_time = self.timer
        #         self.completed = True
        #         self.parentScreen.end_game(
        #             f"Completed!\n\nWell done!\n Your time: {self.parentScreen.ids.timer_id.text}"
        #         )

        #     elif karts[0].hasBurned() and not self.burned:
        #         self.parentScreen.end_game("You have burned!\n\nTry again!")
        #         self.completed_time = self.timer
        #         self.burned = True

    def connectedPlayers(self):
        """Retourne la liste des joueurs connectés."""
        return self._connectedPlayers

    def checkIfNewConnection(self):
        """Appelé à chaque nouvelle factory créée. Vérifie si il y a eu une nouvelle (dé)connection et informe les autre joueurs."""
        for kart in self._game._factory.karts():
            if kart.username() not in self.connectedPlayers():
                self.new_connection(kart.username())
        for player in self.connectedPlayers():
            if player not in list(kart.username() for kart in self._game.karts()):
                self.new_disconnection(player)
        self._connectedPlayers = list(kart.username() for kart in self._game.karts())

    def bind_keyboard(self) -> None:
        self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.keyboard_down)
        self._keyboard.bind(on_key_up=self.keyboard_up)
