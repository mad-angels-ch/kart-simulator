from os import listdir
from typing import List

from kivy.app import App
from kivy.metrics import sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.togglebutton import ToggleButton


class KartSettings(GridLayout):
    karts_list: list
    _chosenKart: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 5
        self.buttons = []
        self.karts_list = self.generateKartsList()
        self._chosenKart = ""

        for k in range(len(self.karts_list)):
            box = BoxLayout(orientation="vertical")
            im = Image(
                source=f"client/Images/karts/{self.karts_list[k]}",
                allow_stretch=False,
                size_hint=(1, 0.9),
            )
            box.add_widget(im)
            b = ToggleButton(
                text=self.karts_list[k][:-4],
                font_size=sp(20),
                size_hint=(1, 0.1),
                group="karts",
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
        return [kart for kart in listdir("client/Images/karts")]

    def updateUserSettings(self, instance) -> None:
        """Met à jour les paramètres du comte du joueur."""
        if self._chosenKart != "":
            app = App.get_running_app()
            data = app.get_userSettings()
            data["kart"] = self._chosenKart
            app.set_userSettings(data)

    def updateChosenKart(self, button) -> None:
        """Met à jour le nom du kart choisi."""
        self._chosenKart = button.text
