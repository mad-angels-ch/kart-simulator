from typing import Callable, Dict, List, Tuple, AnyStr
from socketio import Client, ClientNamespace
from requests import Session
from client.output import kart_simulator
from client.output.outputFactory import OutputFactory

from game import Game, OnCollisionT
from game.objects import Object
from game.events import Event, KartMoveEvent, KartTurnEvent
import lib
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.button import Button

class MultiplayerGame(ClientNamespace):
    _game: Game
    _sio: Client

    def __init__(
        self,
        session: Session,
        server: str,
        name: str,
        output: Callable[[List[Object]], None],
        changeLabelText: Callable[[AnyStr], None],
        parrentScreen: Screen,
        onCollision: OnCollisionT = lambda o, p: None,
        worldVersion_id: "int | None" = None,
    ):
        super().__init__("/kartmultiplayer")
        self.parrentScreen = parrentScreen
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
            self.fatalError(error="Couldn't reach the server. Please check your internet connection and try again.")
        else:
            self.app.start_ks()
            self.start_button = Button(text="start The game!", size_hint=(0.25, 0.1))
            self.start_button.bind(on_press=self.animation)
            self.parrentScreen.ids.noActionBar.add_widget(self.start_button)

    def error(self, error: "None | str" = None) -> None:
        """Gestion des erreurs non fatales"""

    def fatalError(self, error: "None | str" = None) -> None:
        """Gestion des erreurs fatales"""
        if error:
            self._changeLabelText("Fatal error...\n"+error)
            print(error)
            self.disconnect()


    def animation(self, button):
        self.parrentScreen.startingAnimation(start_theGame = self.start)
        self.parrentScreen.ids.noActionBar.remove_widget(self.start_button)
        
    def start(self) -> None:
        self.emit("start")

    def newEvent(self, event: Event) -> None:
        """Fonction permettant la transmition d'inputs du joueur au server"""
        self.emit("", (event.__class__.__name__, event.toTuple()))

    def on_connect(self):
        if self._worldVersion_id == None:
            self.emit("join", self._name, callback=self.fatalError)

        else:
            self.emit(
                "create", (self._name, self._worldVersion_id), callback=self.fatalError
            )

    def on_game_data(self, data: dict):
        """Evènement appelé à chaque nouvelle factory partagée par le serveur.
        Recréé la factory locale en fonction des informations reçues."""
        self._game.minimalImport(data)
        self._game.callOutput()

    def _on_objects_update(self, outputs: Dict[int, Tuple[float, float, float]]):
        """Evènement appelé à chaque nouvelle position d'objets reçus.
        Met la liste des objets à jour en fonction de celles-ci."""
        for formID, newPos in outputs.items():
            obj = self._game.objectByFormID(formID)
            # print(formID)
            obj.set_center(lib.Point(newPos))
            obj.set_angle(newPos[2])
        self._game.callOutput()
        
    def frame_callback(self, output: OutputFactory, objects: List[Object]) -> None:
        pass
