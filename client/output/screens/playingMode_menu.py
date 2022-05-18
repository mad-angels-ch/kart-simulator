import webbrowser
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from .layouts import CustomPopup
from kivy.app import App

Builder.load_file("client/output/screens/playingMode_menu.kv")


class PlayingMode(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

    def ModePopup(self):
        """Ajoute le Popup qui demande à l'utilisateur s'il veut se logger"""
        self.popup = CustomPopup(
            "You must be logged in to play to this mode.",
            functions={"Log In":self.yes,"Sign Up":lambda _:webbrowser.open(f"{self.app.server}/auth/register", autoraise=True), "No": self.redirect}
        )
        self.add_widget(self.popup)

    def yes(self, button) -> None:
        """Appelé si l'utilisateur clique sur 'Log In' sur le popup."""
        self.remove_widget(self.popup)
        App.get_running_app().manager.push("LogIn")

    def redirect(self, button) -> None:
        """Appelé si l'utilisateur clique sur 'No' sur le popup."""
        self.remove_widget(self.popup)
