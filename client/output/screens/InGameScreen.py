from functools import partial
from subprocess import call
from typing import List
from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from client.output.SingleplayerGame import SingleplayerGame
from kivy.app import App
from kivy.uix.label import Label
from kivy.properties import Clock
from kivy.lang import Builder
from kivy.uix.widget import Widget

from client.output.outputFactory import OutputFactory
from game.objects import *

Builder.load_file("client/output/screens/InGameScreen.kv")

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
        
    def quit(self):
        """Nettoyage du canvas de jeu et arrêt de la pendule après la partie"""
        self.ids.noActionBar.canvas.clear()
        
    def pauseMode(self):
        """Appel du mode de pause, utilisé dans le cas d'une partie en solo."""
        self.pauseMenu = PauseMode(
            size=self.app.windowSize())
        self.add_widget(self.pauseMenu)
        
    def resumeGame(self):
        """Reprise de la partie à la fin de la pause. A surcharger dans le cas d'une partie en solo."""
        self.remove_widget(self.pauseMenu)
        
    def endGameMode(self, message):
        """Appel du mode de fin de partie"""
        self.app.game.finish_game()
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
        
    def begin_game(self, start_theGame, dt):
        """Démarrage de la partie"""
        start_theGame()
        
    def startingAnimation(self, start_theGame):
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
        
        Clock.schedule_once(partial(self.begin_game, start_theGame), 6)
        
    def end_game(self, endGameMessage=""):
        """Appel du mode de fin de partie"""
        self.endGameMode(endGameMessage)
    
    # def solo_frameCallback(self, output: OutputFactory, objects: List[Object]) -> None:
    #     """Fonction appellée à chaque frame par output dans le cas d'une partie en solo."""
    #     if output.isInitialized():
    #         self.updateGatesCount(output.getAllGates(), kart_id = output.getAllKarts()[0].formID())
    #         self.updateLapsCount(output.getFinishLine(), kart_id = output.getAllKarts()[0].formID())
    #         self.updateTimer()
    #         self.checkIfGameIsOver(output.getAllKarts(), output.getFinishLine())

    # def updateTimer(self) -> None:
    #     """Mise à jour du timer"""
    #     self.timer += 1 / 60        # 60 pour le nombre de fps
    #     s, mili = divmod(int(1000 * self.timer), 1000)
    #     min, s = divmod(s, 60)
    #     if mili > 100:
    #         self.ids.timer_id.text = f"{min:d}:{s:02d}:{mili:02d}"
    #     else:
    #         self.ids.timer_id.text = f"{min:d}:{s:02d}:0{mili:02d}"

    # def updateLapsCount(self, finishLine: FinishLine, kart_id) -> None:
    #     """Met l'affichage du nombre de tours terminés à jour"""
    #     self.ids.laps_id.text = f"{finishLine.passagesCount(kart_id)}/{finishLine.numberOfLapsRequired()}"

    # def updateGatesCount(self, gatesList: List[Gate], kart_id) -> None:
    #     """Met l'affiche du nombre de portillons (du tour) franchis à jour"""
    #     numberOfGates = len(gatesList)
    #     gatesPassed = (
    #         sum([gate.passagesCount(kart_id) for gate in gatesList])
    #         % numberOfGates
    #     )
    #     self.ids.gates_id.text = f"{gatesPassed}/{numberOfGates}"

    # def checkIfGameIsOver(self, karts: List[Kart], finishLine: FinishLine) -> None:
    #     """Contrôle si la partie est terminée et si oui gère celle-ci"""
    #     if finishLine.completedAllLaps(karts[0].formID()):
    #         self.end_game(
    #             f"Completed!\n\nWell done!\n Your time: {self.ids.timer_id.text}"
    #         )
    #     elif karts[0].hasBurned():
    #         self.end_game("You have burned!\n\nTry again!")
    
    # def multi_frameCallback(self, output: OutputFactory, objects: List[Object]) -> None:
    #     """Fonction appellée à chaque frame par output dans le cas d'une partie en multijoueur."""
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# class KS_screen(Screen):
#     def __init__(self, world, POV, **kw):
#         """Screen responsable d'afficher la partie"""
#         super().__init__(**kw)

#         self.app = App.get_running_app()
#         self.world = world
#         self.POV = POV
#         # Instantiation du canvas de jeu
#         self.game = SingleplayerGame(self.world, POV=self.POV, parentScreen=self)
#         if self.game.theGame:
#             self.ids.noActionBar.add_widget(self.game)
#             # self.start_button = Button(text="start The game!", size_hint=(0.25, 0.1))
#             # self.start_button.bind(on_press=self.startingAnimation)
#             # self.ids.noActionBar.add_widget(self.start_button)
#             self.game.theGame.callOutput()
#             self.startingAnimation()

#     def quit(self):
#         """Nettoyage du canvas de jeu après la partie"""
#         self.game.clear()

#     def pauseMode(self):
#         """Appel du mode de pause"""

#         self.game.play = False
#         self.game.my_clock.unschedule(self.game.nextFrame)
#         self.pauseMenu = PauseMode(
#             size=self.app.windowSize())
#         self.add_widget(self.pauseMenu)

#     def endGameMode(self, message):
#         """Appel du mode de fin de partie"""

#         self.game.play = False
#         self.game.my_clock.unschedule(self.game.nextFrame)
#         self.endGameMenu = EndGameMode()
#         self.endGameMenu.ids.gameOverLabel_id.text = message
#         anim = (
#             Animation(font_size=74, duration=0.1)
#             + Animation(font_size=120, duration=1)
#             + Animation(font_size=120, duration=0.1)
#             + Animation(font_size=74, duration=1)
#         )
#         anim.repeat = True
#         anim.start(self.endGameMenu.ids.gameOverLabel_id)
#         self.add_widget(self.endGameMenu)

#     def begin_game(self, dt):
#         """Démarrage de la partie"""
#         self.game.start_theGame()
 
#     def startingAnimation(self):
#         """Création et affichage de l'animation de début de partie"""
#         # self.ids.noActionBar.remove_widget(self.start_button)
#         start_animation3 = Label(
#             text="3", font_size=0, halign="center", color=(1, 0, 1, 1)
#         )
#         start_animation2 = Label(
#             text="2", font_size=0, halign="center", color=(1, 0, 1, 1)
#         )
#         start_animation1 = Label(
#             text="1", font_size=0, halign="center", color=(1, 0, 1, 1)
#         )
#         start_animationGO = Label(
#             text="GOOOO!!!!", font_size=0, halign="center", color=(1, 0, 1, 1)
#         )

#         self.ids.animationLayout.add_widget(start_animation3)
#         self.ids.animationLayout.add_widget(start_animation2)
#         self.ids.animationLayout.add_widget(start_animation1)
#         self.ids.animationLayout.add_widget(start_animationGO)
#         anim = (
#             Animation(font_size=74, duration=0.5)
#             + Animation(font_size=200, duration=0.5)
#             + Animation(font_size=0, duration=0.5)
#         )
#         anim.start(start_animation3)
#         anim = (
#             Animation(duration=1.5)
#             + Animation(font_size=74, duration=0.5)
#             + Animation(font_size=200, duration=0.5)
#             + Animation(font_size=0, duration=0.5)
#         )
#         anim.start(start_animation2)
#         anim = (
#             Animation(duration=3)
#             + Animation(font_size=74, duration=0.5)
#             + Animation(font_size=200, duration=0.5)
#             + Animation(font_size=0, duration=0.5)
#         )
#         anim.start(start_animation1)
#         anim = (
#             Animation(duration=4.5)
#             + Animation(font_size=74, duration=0.5)
#             + Animation(font_size=400, duration=0.5)
#             + Animation(font_size=0, duration=0.5)
#         )
#         anim.start(start_animationGO)
#         # Appel d'une instance de l'output afin d'afficher le circuit derrière l'animation
#         Clock.schedule_once(self.begin_game, 6)

#     def end_game(self, endGameMessage=""):
#         """Appel du mode de fin de partie"""
#         self.endGameMode(endGameMessage)

#     def resumeGame(self):
#         """Reprise de la partie à la fin de la pause"""

#         self.game.play = True
#         self.game.my_clock.schedule_interval(self.game.nextFrame, 1 / self.game.fps)
#         self.remove_widget(self.pauseMenu)
