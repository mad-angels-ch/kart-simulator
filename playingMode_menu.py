from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from layouts import LogInQuestion
from kivy.app import App

Builder.load_file("playingMode_menu.kv")

class PlayingMode(FloatLayout):
    
    def logInQuestion(self):
        """Ajoute le Popup qui demande à l'utilisateur s'il veut se logger"""
        self.popup=LogInQuestion(self, no=self.no, yes=self.yes)
        self.add_widget(self.popup)
        
    def yes(self):
        """Appelé si l'utilisateur clique sur 'Yes' sur le popup."""
        self.remove_widget(self.popup)
        App.get_running_app().manager.push("")
    
    def no(self):
        """Appelé si l'utilisateur clique sur 'No' sur le popup."""
        self.remove_widget(self.popup)