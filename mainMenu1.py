from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.label import Label
from layouts import LogInQuestion


Builder.load_file("mainMenu1.kv")

class MainMenu1(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
    def callback(self, inst, dt):
        self.app.manager.push("MainMenu")
    
    def logInQuestion(self):
        self.add_widget(LogInQuestion(self))
        