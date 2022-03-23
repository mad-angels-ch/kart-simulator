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
        
    def logInQuestion(self, yes, no):
        """Ajoute le Popup qui demande à l'utilisateur s'il veut se logger"""
        self.popup = LogInQuestion(yes=yes,no=no)
        self.add_widget(self.popup)
        
    def yesPlay(self, button):
        """Appelé si l'utilisateur clique sur 'Yes' sur le popup pour jouer."""
        self.remove_widget(self.popup)
        self.app.manager.push("LogIn")
    
    def noPlay(self, button):
        """Appelé si l'utilisateur clique sur 'No' sur le popup."""
        self.app.manager.push("Playingmode")
        self.remove_widget(self.popup)
        
    def yesSettings(self,button):
        """Appelé si l'utilisateur clique sur 'Yes' sur le popup pour accéder aux 'Settings'."""
        self.remove_widget(self.popup)
        self.app.manager.push("LogIn")
    
    def noSettings(self, button):
        """Appelé si l'utilisateur clique sur 'No' sur le popup."""
        self.app.manager.push("SettingsMenu")
        self.remove_widget(self.popup)