from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout

Builder.load_file("controls.kv")


class Controls(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)