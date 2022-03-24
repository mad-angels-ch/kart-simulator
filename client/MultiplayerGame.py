from typing import Callable, Dict, List, Tuple
from socketio import Client, ClientNamespace
from requests import Session

from game import Game, OnCollisionT
from game.objects import Object
from game.events import Event, KartMoveEvent, KartTurnEvent
import lib
from kivy.uix.label import Label

class MultiplayerGame(ClientNamespace):
    _game: Game
    _sio: Client

    def __init__(
        self,
        session: Session,
        server: str,
        name: str,
        output: Callable[[List[Object]], None],
        onCollision: OnCollisionT = lambda o, p: None,
        worldVersion_id: "int | None" = None,
        errorLabel: "Label |None" = None,
    ):
        super().__init__("/kartmultiplayer")
        self._name = name
        self._worldVersion_id = worldVersion_id
        self._errorLabel = errorLabel
        self._game = Game("", output, onCollision)
        self._sio = Client(http_session=session)
        try:
            self._sio.register_namespace(self)
            self._sio.connect(server, namespaces="/kartmultiplayer")
        except:
            self.fatalError(error="Couldn't reach the server. Please check your internet connection and try again.")

    def error(self, error: "None | str" = None) -> None:
        """Gestion des erreurs non fatales"""

    def fatalError(self, error: "None | str" = None) -> None:
        """Gestion des erreurs fatales"""
        if error:
            self._errorLabel.text = "Fatal error...\n"+error
            print(error)
            self.disconnect()

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

    def on_objects_update(self, outputs: Dict[int, Tuple[float, float, float]]):
        """Evènement appelé à chaque nouvelle position d'objets reçus.
        Met la liste des objets à jour en fonction de celles-ci."""
        for formID, newPos in outputs.items():
            obj = self._game.objectByFormID(formID)
            obj.set_center(lib.Point(newPos))
            obj.set_angle(newPos[2])
        self._game.callOutput()
