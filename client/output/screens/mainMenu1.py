import webbrowser
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import sp
from kivy.uix.floatlayout import FloatLayout

from .layouts import CustomPopup

Builder.load_file("client/output/screens/mainMenu1.kv")


class MainMenu1(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

    def on_kv_post(
        self, a
    ) -> None:  # Appelé dès que le code kivy associé a été traîté (pour que les conditions ne soient pas en dessous du reste du screen)
        try:
            open("client/cookies", "rb")
        except FileNotFoundError:
            self.add_conditions()

    def add_conditions(self) -> None:
        """Ajoute le Popup des conditions d'utilisation."""
        self.popup = CustomPopup(
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.9, 0.4),
            title="Terms and conditions:",
            title_size=sp(32),
            text="Welcome to the kart simulator!\nThis application uses cookies and collects non-anonymous data.\nPlease consent to schare your informations if you want to play.",
            functions={"I Agree":lambda _: self.remove_widget(self.popup),"Quit":lambda _: self.app.stop()}
        )
        self.add_widget(self.popup)

    def callback(self, inst, dt):
        self.app.manager.push("MainMenu")

    def SettingsPopup(self) -> None:
        """Ajoute le Popup qui demande à l'utilisateur s'il veut se logger."""
        self.popup = CustomPopup(
            "You must be logged in to use this function.",
            functions={"Log In":self.yes,"Sign Up":lambda _:webbrowser.open(f"{self.app.server}/auth/register"), "No":self.redirect}
        )
        self.add_widget(self.popup)

    def yes(self, button) -> None:
        """Appelé si l'utilisateur clique sur 'Lof In' sur le popup."""
        self.remove_widget(self.popup)
        App.get_running_app().manager.push("LogIn")

    def redirect(self, button) -> None:
        """Appelé si l'utilisateur clique sur 'No' sur le popup."""
        self.remove_widget(self.popup)
        App.get_running_app().manager.popAll()
