from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.lang import Builder


Builder.load_file("client/output/screens/settings.kv")


class UserSettings(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        
    def logOut(self) -> None:
        self.app.session.post(self.app.server + "/auth/logout")
        self.app.update_userSettings()
        self.app._isLogged = False