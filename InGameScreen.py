from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kart_simulator import MainWidget
from kivy.app import App
from kivy.uix.label import Label
from kivy.properties import Clock
from kivy.lang import Builder

Builder.load_file("InGameScreen.kv")

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
    def __init__(self, world, POV, **kw):
        """Screen responsable d'afficher la partie"""
        super().__init__(**kw)

        self.app = App.get_running_app()
        self.world = world
        self.POV = POV
        # Instantiation du canvas de jeu
        self.game = MainWidget(self.world, POV=self.POV, parentScreen=self)
        if self.game.theGame:
            self.ids.noActionBar.add_widget(self.game)
            # self.start_button = Button(text="start The game!", size_hint=(0.25, 0.1))
            # self.start_button.bind(on_press=self.startingAnimation)
            # self.ids.noActionBar.add_widget(self.start_button)
            self.game.theGame.callOutput()
            self.startingAnimation()

    def quit(self):
        """Nettoyage du canvas de jeu après la partie"""
        self.game.clear()

    def pauseMode(self):
        """Appel du mode de pause"""

        self.game.play = False
        self.game.my_clock.unschedule(self.game.nextFrame)
        self.pauseMenu = PauseMode(
            size=self.app.windowSize())
        self.add_widget(self.pauseMenu)

    def endGameMode(self, message):
        """Appel du mode de fin de partie"""

        self.game.play = False
        self.game.my_clock.unschedule(self.game.nextFrame)
        self.endGameMenu = EndGameMode()
        self.endGameMenu.ids.gameOverLabel_id.text = message
        anim = (
            Animation(font_size=74, duration=0.1)
            + Animation(font_size=120, duration=1)
            + Animation(font_size=120, duration=0.1)
            + Animation(font_size=74, duration=1)
        )
        anim.repeat = True
        anim.start(self.endGameMenu.ids.gameOverLabel_id)
        self.add_widget(self.endGameMenu)

    def begin_game(self, dt):
        """Démarrage de la partie"""
        self.game.start_theGame()

    def startingAnimation(self):
        """Création et affichage de l'animation de début de partie"""
        # self.ids.noActionBar.remove_widget(self.start_button)
        start_animation3 = Label(
            text="3", font_size=0, halign="center", color=(1, 0, 1, 1)
        )
        start_animation2 = Label(
            text="2", font_size=0, halign="center", color=(1, 0, 1, 1)
        )
        start_animation1 = Label(
            text="1", font_size=0, halign="center", color=(1, 0, 1, 1)
        )
        start_animationGO = Label(
            text="GOOOO!!!!", font_size=0, halign="center", color=(1, 0, 1, 1)
        )

        self.ids.animationLayout.add_widget(start_animation3)
        self.ids.animationLayout.add_widget(start_animation2)
        self.ids.animationLayout.add_widget(start_animation1)
        self.ids.animationLayout.add_widget(start_animationGO)
        anim = (
            Animation(font_size=74, duration=0.5)
            + Animation(font_size=200, duration=0.5)
            + Animation(font_size=0, duration=0.5)
        )
        anim.start(start_animation3)
        anim = (
            Animation(duration=1.5)
            + Animation(font_size=74, duration=0.5)
            + Animation(font_size=200, duration=0.5)
            + Animation(font_size=0, duration=0.5)
        )
        anim.start(start_animation2)
        anim = (
            Animation(duration=3)
            + Animation(font_size=74, duration=0.5)
            + Animation(font_size=200, duration=0.5)
            + Animation(font_size=0, duration=0.5)
        )
        anim.start(start_animation1)
        anim = (
            Animation(duration=4.5)
            + Animation(font_size=74, duration=0.5)
            + Animation(font_size=400, duration=0.5)
            + Animation(font_size=0, duration=0.5)
        )
        anim.start(start_animationGO)
        # Appel d'une instance de l'output afin d'afficher le circuit derrière l'animation
        Clock.schedule_once(self.begin_game, 6)

    def end_game(self, endGameMessage=""):
        """Appel du mode de fin de partie"""
        self.endGameMode(endGameMessage)

    def resumeGame(self):
        """Reprise de la partie à la fin de la pause"""

        self.game.play = True
        self.game.my_clock.schedule_interval(self.game.nextFrame, 1 / self.game.fps)
        self.remove_widget(self.pauseMenu)
