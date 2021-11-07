
from kivy.uix.screenmanager import ScreenManager, Screen
from kart_simulator import MainWidget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

#################### Gestion des différents screens ###################

class NavigationScreenManager(ScreenManager):
    screen_stack = []

    def push(self, screen_name):
        if screen_name not in self.screen_stack:
            self.screen_stack.append(self.current)
            self.transition.direction = "left"
            self.current = screen_name

    def pop(self):
        if len(self.screen_stack) > 0:
            screen_name = self.screen_stack[-1]
            del self.screen_stack[-1]
            self.transition.direction = "right"
            self.current = screen_name


class MyScreenManager(NavigationScreenManager):
    pass


class KS_screen(Screen):
    # def on_leave(self):
    pass



class KS(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.aa = MainWidget()
        self.add_widget(self.aa)

    def pause(self, button=None):
        if self.button_text == "Pause":
            self.button_text = "Resume"
            self.aa.pause()
        elif self.button_text == "Resume":
            self.button_text = "Pause"
            self.aa.resume()

    button_text = StringProperty("Pause")

##########################################################################