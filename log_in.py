from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.lang import Builder


Builder.load_file("log_in.kv")


class LogIn(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

    def log_in(self):
        data = {"username" : self.ids.username.text, "password" : self.ids.password.text}
        response = self.app.session.post("http://localhost:5000/auth/login/kart", data=data)
        print(response.json())
