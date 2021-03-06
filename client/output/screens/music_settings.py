from os import listdir, path
from typing import List

from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Rectangle
from kivy.metrics import sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.togglebutton import ToggleButton


class MusicSettings(GridLayout):
    musics_list: list
    _chosenMusic: str
    lastUsedButton: Button

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 5
        self.buttons = []
        self.musics_list = self.generateKartsList()
        self._chosenMusic = ""
        self.lastUsedButton = None

        for k in range(len(self.musics_list)):
            box = BoxLayout(orientation="vertical")
            im = Image(
                source=f"client/Images/MusicImage.png",
                allow_stretch=False,
                size_hint=(1, 0.9),
            )
            box.add_widget(im)
            b = ToggleButton(
                text=self.musics_list[k][:-4],
                font_size=sp(20),
                size_hint=(1, 0.1),
                group="musics",
                on_press=self.updateChosenKart,
            )
            box.add_widget(b)
            self.add_widget(box)
            self.buttons.append(b)

        self.add_widget(
            Button(
                text="Save my choice",
                font_size=sp(20),
                on_press=self.updateUserSettings,
            )
        )

    def generateKartsList(self) -> List:
        """Génère la liste des karts disponibles."""
        return [music for music in listdir("client/sounds/music")]

    def updateUserSettings(self, instance) -> None:
        """Met à jour les paramètres du comte du joueur."""
        app = App.get_running_app()
        data = app.get_userSettings()
        data["music"] = self._chosenMusic
        app.set_userSettings(data)

    def updateChosenKart(self, button) -> None:
        """Met à jour le nom de la musique choisie et en joue un extrait."""
        self._chosenMusic = button.text
        if button == self.lastUsedButton:
            if self.music.state == "play":
                self.music.stop()
            else:
                self.music.play()
        else:
            # Enlève la couleur sur l'ancienne musique et la rajoute sur la nouvelle
            if self.lastUsedButton != None:
                self.lastUsedButton.parent.canvas.before.clear()
                self.music.stop()
            with button.parent.canvas.before:
                Color(rgba=(0, 0, 1, 0.25))
                Rectangle(size=button.parent.size, pos=button.parent.pos)

            musicPath = path.join("client/sounds/music", self._chosenMusic) + ".wav"
            self.music = SoundLoader.load(musicPath)
            self.music.volume = 1
            self.music.play()
            self.music.loop = True

            self.lastUsedButton = button
