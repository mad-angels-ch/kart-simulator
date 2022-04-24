import json
from mimetypes import init
from os import listdir
from typing import List
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.lang import Builder


Builder.load_file("client/output/screens/gamesResults.kv")


class Results(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        
    def search_games(self) -> None:
        """Recherche les parties correspondant aux critères choisis et affiche les résultats"""
        chosenOptions = {}
        if self.ids.worldVersion_id.text:
            chosenOptions["worldVersion_id"]=self.ids.worldVersion_id.text
        if self.ids.world.text:
            with open("client/worlds.json", "r", encoding="utf8") as f:
                worlds = json.loads(f.read())
            world_id = worlds[self.ids.world.text]["id"]
            chosenOptions["world_id"]=world_id
        if self.ids.maxGames.text:
            chosenOptions["maxGame"]=self.ids.maxGames.text
        if self.ids.maxPlayers.text:
            chosenOptions["maxPlayers"]=self.ids.maxPlayers.text
        if self.ids.minPlayers.text:
            chosenOptions["minPlayers"]=self.ids.minPlayers.text
        if self.ids.my_games.state == "down":
            result = self.app.session.get(self.app.server + "/games/kart/mygames.json", params=chosenOptions)
            if result.status_code == 400:
                pass
            else:
                print(result.json())

        else:
            if self.ids.username.text:
                chosenOptions["username"]=self.ids.username.text
            result = self.app.session.get(self.app.server + "/games/kart/bestgames.json", params=chosenOptions)
            if result.status_code == 400:
                pass
            else:
                print(result.json())
                
    def generateWorldsList(self) -> list:
        """Génère la liste des curcuits jouables"""
        return [world[:-5] for world in listdir("client/worlds")]
        

            


