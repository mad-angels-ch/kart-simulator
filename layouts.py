
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kart_simulator import MainWidget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.uix.dropdown import DropDown
from action_bar import BoxLayoutWithActionBar

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
    pass
        




class KS(BoxLayout):
    def __init__(self,world=None, **kwargs):
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
    
    
class MainMenu2(FloatLayout):
    chosen_world = "2triangles.json"

##########################################################################