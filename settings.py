from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.lang import Builder


Builder.load_file("settings.kv")


class UserSettings(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)