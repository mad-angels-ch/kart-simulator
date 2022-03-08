from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.uix.button import Button
from kivy.lang import Builder


Builder.load_file("mainMenu1.kv")

class MainMenu1(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def callback(self, inst, dt):
        App.get_running_app().manager.push("MainMenu")