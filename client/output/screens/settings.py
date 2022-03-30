from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.lang import Builder

from client.output.screens.layouts import CustomPopup


Builder.load_file("client/output/screens/settings.kv")


class UserSettings(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        
    def SettingsPopup(self):
        """Ajoute le Popup qui demande à l'utilisateur s'il veut se logger"""
        self.popup=CustomPopup("You must be logged in to use this function.",func1=self.yes,func1_name="Log In",func2=self.redirect,func2_name="No")
        self.add_widget(self.popup)
        
    def yes(self, button):
        """Appelé si l'utilisateur clique sur 'Log In' sur le popup."""
        self.remove_widget(self.popup)
        App.get_running_app().manager.push("LogIn")
    
    def redirect(self, button):
        """Appelé si l'utilisateur clique sur 'No' sur le popup."""
        self.remove_widget(self.popup)
        App.get_running_app().manager.popAll()
        
    def updatePOVSettings(self, newPOV):
        data = self.app.get_userSettings()
        data["pov"] = newPOV
        self.app.set_userSettings(data)
        