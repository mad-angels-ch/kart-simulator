from typing import AnyStr, Callable, Dict, List, Tuple

import click
import engineio
from client.output.screens.layouts import CustomPopup
import lib
from game import Game, OnCollisionT
from game.events import Event
from game.objects import FinishLine, Gate, Kart, Object
from game.objects.Kart import Kart
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.button import Button
from requests import Session
from socketio import Client, ClientNamespace
from socketio.exceptions import BadNamespaceError

from client.output.outputFactory import OutputFactory
from client.output.screens.InGameScreen import KS_screen, WaitingRoom


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
        self.pauseMode = False
        self.parentScreen = parentScreen
        self._name = name
        self._worldVersion_id = worldVersion_id
        self._changeLabelText = changeLabelText
        output.set_frameCallback(self.frame_callback)
        self._game = Game("", output, onCollision)
        self._sio = Client(http_session=session)
        self.app = App.get_running_app()
        self._joiningError = False
        try:
            self._sio.register_namespace(self)
            self._sio.connect(server, namespaces="/kartmultiplayer")
        # except KeyError:
        # pass
        except:
            self.fatalError(
                error="Couldn't reach the server. Please check your internet connection and try again."
            )
        else:
            self._moving = False
            self._rotating = False  # Pour ne pas surcharger le serveur avec des events, un seul event est émi lorsqu'une touche pour avancer ou tourner est émi et un seul autre lorsqu'elle est relâchée.
            self._connectedPlayers = []
            self.app.start_ks()
            self.waitingScreen = WaitingRoom(self._name, size_hint=(1, 1))
            self.parentScreen.add_widget(self.waitingScreen)
            self.timer = 0
            self.my_clock = Clock

        self.y = 0
        # Pour une raison inconnue, lors du redimensionnement d'une fenêtre (qui n'arrive normalement pas car le jeu est par défaut en plein écran),
        # kivy essaie de retrouver la "hauteur" "self.y" de cette classe alors qu'elle n'est en rien liée à l'application graphique...
        # N'ayant pas réussi à régler le problème autrement, nous avons créé la méthode to_window() et l'attribut "y" qui règlent le problème.

    from .output.multi_user_actions import (
        keyboard_closed,
        keyboard_down,
        keyboard_up,
        touch_down,
        touch_up,
    )

    def to_window(self, a, b):
        # c.f. commentaire de self.y ci-dessus
        return self.app.windowSize()

    def updateInfos(self, dt):
        """Met à jour les information affichées sur l'écran de jeu (timer, laps, gates)"""
        self.parentScreen.updateLapsAndGatesCount(
            self._game.objectsFactory(), self.myKart()
        )
        self.checkIfGameIsOver(finishLine=self._game.finishLine())
        self.timer += 1 / 60
        self.parentScreen.updateTimer(self.timer)

    def change_gameState(self) -> None:
        """Change l'état du jeu: pause ou jeu"""
        if not self.pauseMode:
            self.pauseMode = True
            self.parentScreen.pauseMode()
        else:
            self.pauseMode = False
            self.parentScreen.resumeGame()
            if self.myKart():
                self.myKart().set_image(self.app.get_userSettings()["kart"])

    def error(self, error: "None | str" = None) -> None:
        """Gestion des erreurs non fatales"""
        print(error)

    def fatalError(self, error: "None | str" = None) -> None:
        """Gestion des erreurs fatales"""
        if error:
            self._changeLabelText("Fatal error...\n" + error, 6)
            print(error)
            self.disconnect()

    def joiningError(self, error: "None | str" = None) -> None:
        """Gestion des erreur d'entrées en parties"""
        if error:
            self.add_reconnectionPopup(error=error)
            # self.fatalError(error=error)
            # raise KeyError
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

    def start_theGame(self):
        """Appelé à la fin du compteur."""
        self.play = True
        self.my_clock.schedule_interval(
            self.updateInfos, 1 / 60
        )  # Initialise la pendule qui compte le temps de la partie.

    def on_countdown(self):
        self.executeInMainKivyThread(
            self.parentScreen.startingAnimation, start_theGame=self.start_theGame
        )
        self.executeInMainKivyThread(
            self.parentScreen.remove_widget, self.waitingScreen
        )

    def on_passage(self, gate, kart, count) -> None:
        """Evènement appelé à chaque fois qu'un kart passe une gate"""
        self._game.objectByFormID(gate).set_passagesCount(kart, count)
        self._game.objectByFormID(kart).set_lastGate(self._game.objectByFormID(gate))

    def on_burned(self, kart) -> None:
        """Evénement émit à chaque kart brûlé.
        Cette méthode peut être appelée plusieurs fois par kart"""
        self._game.objectByFormID[kart].burn()

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

    def new_connection(self, player: str) -> None:
        self.waitingScreen.set_laps(
            self._game.finishLine().numberOfLapsRequired()
        )  # pas faisable à la création de waitingScreen car _game était en train d'être créé dans un thread parallèle.
        self.waitingScreen.add_player(player)

    def new_disconnection(self, player: str) -> None:
        self.waitingScreen.remove_player(player)

    def on_disconnect(self) -> None:
        self._rotating = False
        self._moving = False
        print("Connection perdue")
        if self.play:
            self.executeInMainKivyThread(self.add_reconnectionPopup)

    def quitTheGame(self) -> None:
        """Quitte la partie"""
        self.play = False
        self.disconnect()
        self.app.manager.popAll()

    def finish_game(self) -> None:
        """Arrêt de la pendule. Appelé dès la fin de la partie."""
        self.my_clock.unschedule(self.updateInfos)

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

    def checkIfGameIsOver(self, finishLine: FinishLine) -> None:
        """Contrôle si la partie est terminée et si oui gère celle-ci"""
        if finishLine.completedAllLaps(self.myKart().formID()):
            self.parentScreen.end_game(
                f"Completed!\n\nWell done!\n Your time: {self.parentScreen.ids.timer_id.text}"
            )

        elif self.myKart().hasBurned():
            self.parentScreen.end_game("You have burned!\n\nDo better next time!")

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

    def add_reconnectionPopup(self, error: str = "") -> None:
        self.popup = CustomPopup(
            error + "\n" + "Do you want to try again?",
            func1=lambda _: self.emit("join", self._name, callback=self.joiningError),
            func1_name="Yes",
            func2=self.no,
            func2_name="No",
        )
        self.parentScreen.add_widget(self.popup)

    def try_reconnection(self, button=None) -> None:
        """Appelé si le joueur essaie de se reconnecter à la partie en appuyant sur le bouton <yes> du popup."""
        self.emit("join", self._name, callback=self.joiningError)
        self.parentScreen.remove_widget(self.popup)

    def no(self, b):
        """Appelé si le joueur renonce à se reconnecter à la partie en appuyant sur le bouton <no> du popup."""
        self.parentScreen.remove_widget(self.popup)
        self.quitTheGame()
