from functools import partial
from random import randrange

from game.objects import *
from kivy.animation import Animation
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import sp
from kivy.properties import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

Builder.load_file("client/output/screens/InGameScreen.kv")


class WaitingRoom(FloatLayout):
    def __init__(self, gameName, **kwargs):
        super().__init__(**kwargs)
        self.is_initialized = False
        self.ids.game_info.text += f"[color=#ff0000]{gameName}[/color]\n"
        self.entries = [
            "finally got up and joined the game !",
            "wants to loose another game !",
            "is ready for the fight !",
            ", we were waiting for you !",
            "has found his way to heaven !",
        ]
        self.exits = [
            "remembered he had a bac to study...",
            "got cought by the philosophy teacher...",
            "got scared by his oponents...",
            "left us. RIP.",
            "swung to the dark side...",
        ]


    def set_laps(self, laps: int) -> None:
        """Met à jour les informations de la partie."""
        if not self.is_initialized:
            self.ids.game_info.text += f"° Number of laps: [color=#ff0000]{laps}[/color]\n"
            self.is_initialized = True

    def add_player(self, player: str):
        """Ajoute un joueur à la liste lors d'une connection."""
        if player in ["lj44", "Noe"]:
            self.ids.game_info.text += f"\n --> {player} THE BOSS IS IN THE PLACE !"
        elif player in ["H2PtCl6"]:
            self.ids.game_info.text += "\n --> Prof. Manganese is in the place !"
        elif player in ["CHAJ", "chaj", "johnschmidt"]:
            self.ids.game_info.text += (
                f"\n --> Bienvenue {player}. Ce projet mérite un 6."
            )
        else:
            self.ids.game_info.text += f"\n --> {player} {self.entries[randrange(5)]}"

    def remove_player(self, player: str):
        """Retire un joueur de la liste lors d'une déconnection."""
        self.ids.game_info.text += f"\n --> {player} {self.exits[randrange(5)]}"


class EndGameMode(FloatLayout):
    """Menu de fin de partie"""

    pass


class PauseMode(FloatLayout):
    def __init__(self, size, **kwargs):
        """Menu de pause"""
        self.width = size[0]
        self.height = size[1]
        super().__init__(**kwargs)


class KS_screen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        """Screen responsable d'afficher la partie"""
        self.widget = Widget()
        self.ids.noActionBar.add_widget(self.widget)
        self.timer = 0
        self.app = App.get_running_app()

    def quit(self) -> None:
        """Nettoyage du canvas de jeu et arrêt de la pendule après la partie"""
        self.ids.noActionBar.canvas.clear()

    def pauseMode(self) -> None:
        """Appel du mode de pause, utilisé dans le cas d'une partie en solo."""
        self.pauseMenu = PauseMode(size=self.app.windowSize())
        self.add_widget(self.pauseMenu)

    def resumeGame(self) -> None:
        """Reprise de la partie à la fin de la pause. A surcharger dans le cas d'une partie en solo."""
        self.remove_widget(self.pauseMenu)

    def endGameMode(self, message) -> None:
        """Appel du mode de fin de partie"""
        self.app.game.finish_game()
        self.endGameMenu = EndGameMode()
        self.endGameMenu.ids.gameOverLabel_id.text = message
        anim = (
            Animation(font_size=sp(100), duration=0.1)
            + Animation(font_size=sp(150), duration=1)
            + Animation(font_size=sp(150), duration=0.1)
            + Animation(font_size=sp(100), duration=1)
        )
        anim.repeat = True
        anim.start(self.endGameMenu.ids.gameOverLabel_id)
        self.add_widget(self.endGameMenu)

    def begin_game(self, start_theGame, dt) -> None:
        """Démarrage de la partie"""
        start_theGame()

    def startingAnimation(self, start_theGame) -> None:
        """Création et affichage de l'animation de début de partie"""
        time = 0
        for text in ["3", "2", "1", "GOOOO!!!!"]:
            start_animation = Label(
                text=text, font_size=0, halign="center", color=(0, 1, 0, 1)
            )

            self.ids.animationLayout.add_widget(start_animation)
            anim = (
                Animation(duration=1.5 * time)
                + Animation(font_size=sp(200), duration=0.5)
                + Animation(font_size=sp(250), duration=0.5)
                + Animation(font_size=0, duration=0.5)
            )
            anim.start(start_animation)
            time += 1

        Clock.schedule_once(partial(self.begin_game, start_theGame), 6)

    def end_game(self, endGameMessage="") -> None:
        """Appel du mode de fin de partie"""
        self.endGameMode(endGameMessage)

    def updateLapsAndGatesCount(self, factory: ObjectFactory, kart: Kart) -> None:
        """Met l'affichage du nombre de tours et du nombre de portillons à jour"""
        finishLine = factory.finishLine()
        self.ids.laps_id.text = f"{finishLine.passagesCount(kart.formID())}/{finishLine.numberOfLapsRequired()}"
        self.ids.gates_id.text = (
            f"{kart.lastGatePosition()}/{finishLine.numberOfGates()}"
        )

    def updateTimer(self, time: float) -> None:
        """Mise à jour du timer"""
        s, mili = divmod(int(1000 * time), 1000)
        min, s = divmod(s, 60)
        if mili > 100:
            self.ids.timer_id.text = f"{min:d}:{s:02d}:{mili:02d}"
        else:
            self.ids.timer_id.text = f"{min:d}:{s:02d}:0{mili:02d}"
