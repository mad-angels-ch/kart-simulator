from typing import Callable, Dict, List, Tuple, AnyStr
import click
from socketio import Client, ClientNamespace
from requests import Session

from game import Game, OnCollisionT
from game.objects import Object
from game.events import Event, KartMoveEvent, KartTurnEvent
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
    _charged: bool = False

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
            self.fatalError(
                error="Couldn't reach the server. Please check your internet connection and try again."
            )
        else:
            self.app.start_ks()
            
        self.y = 0      # Pour une raison inconnue, lors du redimensionnement d'une fenêtre (qui n'arrive normalement pas car le jeu est par défaut en plein écran), kivy essaie de retrouver la "hauteur" "self.y" de cette classe alors qu'elle n'est en rien liée à l'application graphique... n'ayant pas réussi à régler le problème autrement, nous avons créé la méthode to_window() et l'attribut "y" qui règlent le problème.
        
    from .output.multi_user_actions import (
        keyboard_closed,
        keyboard_down,
        keyboard_up,
        touch_up,
        touch_down,
    )
    
    def to_window(self,a,b):
        #c.f. commentaire de self.y ci-dessus
        return self.app.windowSize()
    
    def error(self, error: "None | str" = None) -> None:
        """Gestion des erreurs non fatales"""

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

    def animation(self, button):
        self.parrentScreen.startingAnimation(start_theGame=self.start)
        self.parrentScreen.ids.noActionBar.remove_widget(self.start_button)

    def start(self) -> None:
        self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.keyboard_down)
        self._keyboard.bind(on_key_up=self.keyboard_up)
        self.emit("start")

    def newEvent(self, event: Event) -> None:
        """Fonction permettant la transmition d'inputs du joueur au server"""
        print("New event")
        self.emit("event", (event.__class__.__name__, event.toTuple()))

    def on_connect(self):
        if self._worldVersion_id == None:
            self.emit("join", self._name, callback=self.joiningError)

        else:
            self.start_button = Button(text="Start the game!", size_hint=(0.25, 0.1))       # Création du bouton qui permet de démarrer la partie
            self.start_button.bind(on_press=self.animation)
            self.parrentScreen.ids.noActionBar.add_widget(self.start_button)
            
            self.emit(
                "create",
                (self._name, self._worldVersion_id),
                callback=self.joiningError,
            )                                                                               # Informe le serveur de la création d'une partie
            self._worldVersion_id = None

    def on_game_data(self, data: dict):
        """Evènement appelé à chaque nouvelle factory partagée par le serveur.
        Recréé la factory locale en fonction des informations reçues."""
        self._game.minimalImport(data)
        self._charged = True
        self.callOutput()

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

    def frame_callback(self, output: OutputFactory, objects: List[Object]) -> None:
        pass

    def callOutput(self) -> None:
        if self._charged:
            Clock.schedule_once(lambda _: self._game.callOutput(), 0)
