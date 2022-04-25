import os
import os.path

try:
    import client.worlds
except ModuleNotFoundError:
    os.makedirs("client/worlds")
    import client.worlds

from game.objects import *
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup


class CustomPopup(Popup):
    """Classe qui demande à l'utilisateur s'il veut se connecter à son compte ou non, puis se détruit."""

    def __init__(
        self,
        title="",
        text="",
        func1=None,
        func1_name="",
        func2=None,
        func2_name="",
        **kwargs
    ):
        super().__init__(title=title, **kwargs)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.7}
        self.size_hint = (0.5, 0.2)
        box1 = BoxLayout(orientation="vertical")
        app = App.get_running_app()
        box1.add_widget(Label(text=text))
        box2 = BoxLayout(orientation="horizontal")
        box1.add_widget(box2)
        if func1:
            box2.add_widget(Button(text=func1_name, on_press=func1))
        if func2:
            box2.add_widget(Button(text=func2_name, on_press=func2))
        self.content = box1
