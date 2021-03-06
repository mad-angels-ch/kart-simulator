from distutils.log import error
from logging import warning
from typing import AnyStr, Callable, Dict, List, Tuple

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
from client.output.screens.layouts import CustomPopup


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
        self.start_button = None
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
            self._rotating = False  # Pour ne pas surcharger le serveur avec des events, un seul event est ??mi lorsqu'une touche pour avancer ou tourner est ??mi et un seul autre lorsqu'elle est rel??ch??e.
            self._connectedPlayers = []
            self.popup = None
            self.app.start_ks()
            self.waitingScreen = WaitingRoom(self._name, size_hint=(1, 1))
            self.parentScreen.add_widget(self.waitingScreen)
            self.timer = 0
            self.my_clock = Clock

        self.y = 0
        # Pour une raison inconnue, lors du redimensionnement d'une fen??tre (qui n'arrive normalement pas car le jeu est par d??faut en plein ??cran),
        # kivy essaie de retrouver la "hauteur" "self.y" de cette classe alors qu'elle n'est en rien li??e ?? l'application graphique...
        # N'ayant pas r??ussi ?? r??gler le probl??me autrement, nous avons cr???? la m??thode to_window() et l'attribut "y" qui r??glent le probl??me.

    from .output.multi_user_actions import (
        keyboard_closed,
        keyboard_down,
        keyboard_up,
        touch_down,
        touch_up,
    )

    def to_window(self, a, b) -> None:
        # c.f. commentaire de self.y ci-dessus
        return self.app.windowSize()

    def updateInfos(self, dt) -> None:
        """Met ?? jour les information affich??es sur l'??cran de jeu (timer, laps, gates)"""
        self.parentScreen.updateLapsAndGatesCount(
            self._game.objectsFactory(), self.myKart()
        )
        self.checkIfGameIsOver(finishLine=self._game.finishLine())
        self.timer += 1 / 60
        self.parentScreen.updateTimer(self.timer)

    def change_gameState(self) -> None:
        """Change l'??tat du jeu: pause ou jeu"""
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
        warning(error)

    def fatalError(self, error: "None | str" = None) -> None:
        """Gestion des erreurs fatales"""
        if error:
            self._changeLabelText("Fatal error...\n" + error, 6)
            self.disconnect()

    def joiningError(self, error: "None | str" = None) -> None:
        """Gestion des erreur d'entr??es en parties"""
        if error:
            self.executeInMainKivyThread(self.add_reconnectionPopup,error)

    def start(self) -> None:
        self.emit("start")
        self.waitingScreen.remove_widget(self.start_button)
        self.start_button = None

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
            font_size="20sp",
            size_hint=(0.25, 0.1),
            pos_hint={"center_x": 0.5, "y": 0.1},
        )  # Cr??ation du bouton qui permet de d??marrer la partie
        self.start_button.bind(on_press=lambda _: self.start())
        self.waitingScreen.add_widget(self.start_button)

    def on_connect(self) -> None:
        self.executeInMainKivyThread(self.bind_keyboard)
        if self._worldVersion_id == None:
            self.emit("join", self._name, callback=self.joiningError)
        else:
            self.executeInMainKivyThread(self.createStartButton)
            self.emit(
                "create",
                (self._name, self._worldVersion_id),
                callback=self.joiningError,
            )  # Informe le serveur de la cr??ation d'une partie
            self._worldVersion_id = None

    def start_theGame(self) -> None:
        """Appel?? ?? la fin du compteur."""
        self.play = True
        self.my_clock.schedule_interval(
            self.updateInfos, 1 / 60
        )  # Initialise la pendule qui compte le temps de la partie.

    def on_countdown(self) -> None:
        self.executeInMainKivyThread(
            self.parentScreen.startingAnimation, start_theGame=self.start_theGame
        )
        self.executeInMainKivyThread(
            self.parentScreen.remove_widget, self.waitingScreen
        )

    def on_passage(self, gate, kart, count) -> None:
        """Ev??nement appel?? ?? chaque fois qu'un kart passe une gate"""
        self._game.objectByFormID(gate).set_passagesCount(kart, count)
        self._game.objectByFormID(kart).set_lastGate(self._game.objectByFormID(gate))

    def on_burned(self, kart) -> None:
        """Ev??nement ??mit ?? chaque kart br??l??.
        Cette m??thode peut ??tre appel??e plusieurs fois par kart"""
        if not self._game.objectByFormID(kart).hasBurned():
            self._game.objectByFormID(kart).burn()

    def on_game_data(self, data: dict) -> None:
        """Ev??nement appel?? ?? chaque nouvelle factory partag??e par le serveur.
        Recr???? la factory locale en fonction des informations re??ues."""
        self.executeInMainKivyThread(self._game.minimalImport, data)
        self.executeInMainKivyThread(self.get_myKart)
        self.executeInMainKivyThread(self.checkIfNewConnection)

    def on_objects_update(self, outputs: Dict[int, Tuple[float, float, float]]) -> None:
        """Ev??nement appel?? ?? chaque nouvelle position d'objets re??us.
        Met la liste des objets ?? jour en fonction de celles-ci."""
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
        )  # pas faisable ?? la cr??ation de waitingScreen car _game ??tait en train d'??tre cr???? dans un thread parall??le.
        self.waitingScreen.add_player(player)

    def new_disconnection(self, player: str) -> None:
        self.waitingScreen.remove_player(player)

    def on_disconnect(self) -> None:
        self._rotating = False
        self._moving = False
        if self.play:
            self.executeInMainKivyThread(self.try_reconnection)

    def quitTheGame(self) -> None:
        """Quitte la partie"""
        self.play = False
        self.keyboard_closed()
        self.disconnect()
        self.app.manager.popAll()

    def finish_game(self) -> None:
        """Arr??t de la pendule. Appel?? d??s la fin de la partie."""
        self.my_clock.unschedule(self.updateInfos)

    def executeInMainKivyThread(self, function, *args, **kwargs) -> None:
        Clock.schedule_once(lambda _: function(*args, **kwargs), 0)

    def frame_callback(self, output: OutputFactory, objects: List[Object]) -> None:
        pass

    def callOutput(self) -> None:
        self.executeInMainKivyThread(self._game.callOutput)

    def myKart(self) -> Kart:
        """Retourne le kart associ?? au joueur connect??."""
        return self._myKart

    def get_myKart(self) -> int:
        for kart in self._game.karts():
            if kart.username() == self.app.get_userSettings()["username"]:
                self._myKart = kart  # R??cup??re le kart associ?? au joueur connect??.

    def checkIfGameIsOver(self, finishLine: FinishLine) -> None:
        """Contr??le si la partie est termin??e et si oui g??re celle-ci"""
        if finishLine.completedAllLaps(self.myKart().formID()):
            self.parentScreen.end_game(
                f"Completed!\n\nWell done!\n Your time: {self.parentScreen.ids.timer_id.text}"
            )

        elif self.myKart().hasBurned():
            self.parentScreen.end_game("You have burned!\n\nDo better next time!")

    def connectedPlayers(self) -> List:
        """Retourne la liste des joueurs connect??s."""
        return self._connectedPlayers

    def checkIfNewConnection(self) -> None:
        """Appel?? ?? chaque nouvelle factory cr????e. V??rifie si il y a eu une nouvelle (d??)connection et informe les autre joueurs."""
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
        if not self.popup:
            self.popup = CustomPopup(
                "Connection lost:\n" + error + "\n" + "Do you want to try to reconnect?",
                functions={"Yes":self.try_reconnection,"No":self.no, "Quit":self.quit}
            )
            self.parentScreen.add_widget(self.popup)

    def try_reconnection(self, button=None) -> None:
        """Appel?? si le joueur essaie de se reconnecter ?? la partie en appuyant sur le bouton <yes> du popup."""
        if self.popup:
            self.parentScreen.remove_widget(self.popup)
            self.popup = None
        try:
            self.emit("join", self._name, callback=self.joiningError)
        except BadNamespaceError as e:
            warning(e)
        except BaseException as e:
            error(e)
        
    def quit(self, b) -> None:
        """Appel?? si le joueur renonce ?? se reconnecter ?? la partie en appuyant sur le bouton <Quit> du popup."""
        self.parentScreen.remove_widget(self.popup)
        self.popup = None
        self.quitTheGame()
        
    def no(self, b) -> None:
        """Appel?? si le joueur renonce ?? se reconnecter ?? la partie en appuyant sur le bouton <no> du popup."""
        self.parentScreen.remove_widget(self.popup)
        self.popup = None
