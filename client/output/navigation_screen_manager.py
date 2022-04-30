from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager


class NavigationScreenManager(ScreenManager):
    screen_stack = []

    def push(self, screen_name) -> None:
        if screen_name not in self.screen_stack:
            self.screen_stack.append(self.current)
            self.transition.direction = "left"
            self.current = screen_name

    def pop(self) -> None:
        if len(self.screen_stack) > 0:
            screen_name = self.screen_stack[-1]
            del self.screen_stack[-1]
            self.transition.direction = "right"
            self.current = screen_name

    def popAll(self) -> None:
        if self.current_screen.name != "MainMenu":
            screen_name = self.screen_stack[0]
            del self.screen_stack[0:]
            self.transition.direction = "right"
            self.current = screen_name


class MyScreenManager(NavigationScreenManager):
    """Manager qui gère les entrées et sorties des screens"""

    pass
