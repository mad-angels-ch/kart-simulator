from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.label import Label
from .layouts import CustomPopup


Builder.load_file("client/output/screens/mainMenu1.kv")

class MainMenu1(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        
    def callback(self, inst, dt):
        self.app.manager.push("MainMenu")
        
    def SettingsPopup(self):
        """Ajoute le Popup qui demande à l'utilisateur s'il veut se logger."""
        self.popup=CustomPopup("You must be logged in to use this function.",func1=self.yes,func1_name="Log In",func2=self.redirect,func2_name="No")
        self.add_widget(self.popup)
        
    def yes(self, button):
        """Appelé si l'utilisateur clique sur 'Lof In' sur le popup."""
        self.remove_widget(self.popup)
        App.get_running_app().manager.push("LogIn")
    
    def redirect(self, button):
        """Appelé si l'utilisateur clique sur 'No' sur le popup."""
        self.remove_widget(self.popup)
        App.get_running_app().manager.popAll()