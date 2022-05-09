import pickle, requests
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.lang import Builder


Builder.load_file("client/output/screens/log_in.kv")


class LogIn(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

    def log_in(self) -> None:
        data = {"username": self.ids.username.text, "password": self.ids.password.text}
        try:
            response = self.app.session.post(
                self.app.server + "/auth/login/kart", data=data
            )
        except requests.ConnectionError:
            self.ids.errorLabel.text = "Couldn't reach the server. Please check your internet connection and try again."
        else:
            if response.json().get("error", 0):
                self.ids.errorLabel.text = response.json()["error"]
            else:
                with open(self.app.cookiesPath, "wb") as f:
                    pickle.dump(self.app.session.cookies, f)
                self.app._isLogged = True
                self.app.manager.pop()
        self.app.update_userSettings()
