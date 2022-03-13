from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from os import listdir
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.app import App

class KartSettings(GridLayout):
    karts_list: list
    _chosenKart: str
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 5
        self.buttons = []
        self.karts_list = self.generateKartsList()
        self._chosenKart = ""
        
        for k in range(len(self.karts_list)):
            box = BoxLayout(orientation='vertical')
            im = Image(source=f"client/Images/karts/{self.karts_list[k]}", allow_stretch = False, size_hint=(1, .9))
            box.add_widget(im)
            b=ToggleButton(text=self.karts_list[k][:-4], size_hint=(1, .1), group = "karts", on_press=self.updateChosenKart)
            box.add_widget(b)
            self.add_widget(box)
            self.buttons.append(b)
            
        self.add_widget(Button(text="Save my choice",on_press=self.updateUserSettings))

    def generateKartsList(self):
        """Génère la liste des karts disponibles."""
        return [kart for kart in listdir("client/Images/karts")]
    
    def updateUserSettings(self, instance):
        """Met à jour les paramètres du comte du joueur."""
        if self._chosenKart != "":
            app = App.get_running_app()
            data = app.get_userSettings()
            data["kart"] = self._chosenKart
            app.session.put("http://localhost:5000/auth/myaccount/kart.json", data)
            app.update_userSettings()
            
    def updateChosenKart(self,button):
        """Met à jour le nom du kart choisi."""
        self._chosenKart = button.text