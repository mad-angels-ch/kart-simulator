from cgitb import text
import json
from mimetypes import init
from os import listdir
from turtle import width
from typing import List
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.button import Button

from datetime import datetime, timedelta

Builder.load_file("client/output/screens/gamesResults.kv")


class Results(FloatLayout):
    """Classe qui affiche la page de résultats.
    Dérivée de kivy.uix.ScrollView pour avoir la possiblilté de "scroll" vers le bas et afficher toutes les parties.
    Contient un Floatlayout dans lequel tous les autres widgets seront ajoutés, car ScrollView n'accepte qu'ne seil widget enfant."""

    _widgets: list  # liste de tous les widgets Label présents dans le tableau, à enlever à chaque nouvelle recherche de parties.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self._widgets = []
        # self.add_widget(ScrollView(size_hint=(1, None), size=(Window.width, Window.height)))

    def search_games(self) -> None:
        """Recherche les parties correspondant aux critères choisis et affiche les résultats"""
        chosenOptions = {}
        if self.ids.worldVersion_id.text:
            chosenOptions["worldVersion_id"] = self.ids.worldVersion_id.text
        if self.ids.world.text != "All Worlds":
            with open("client/worlds.json", "r", encoding="utf8") as f:
                worlds = json.loads(f.read())
            world_id = worlds[self.ids.world.text]["id"]
            chosenOptions["world_id"] = world_id
        if self.ids.maxGames.text:
            chosenOptions["maxGame"] = self.ids.maxGames.text
        if self.ids.maxPlayers.text:
            chosenOptions["maxPlayers"] = self.ids.maxPlayers.text
        if self.ids.minPlayers.text:
            chosenOptions["minPlayers"] = self.ids.minPlayers.text
        if self.ids.my_games.state == "down":
            result = self.app.session.get(
                self.app.server + "/games/kart/mygames.json", params=chosenOptions
            )
            if result.status_code == 400:
                pass
            else:
                print(result.json())
                self.generateTables(result.json())

        else:
            if self.ids.username.text:
                chosenOptions["username"] = self.ids.username.text
            result = self.app.session.get(
                self.app.server + "/games/kart/bestgames.json", params=chosenOptions
            )
            if result.status_code == 400:
                pass
            else:
                print(result.json())
                self.generateTables(result.json())

    def generateTables(self, result: List[dict]) -> None:
        """Génère les nouvelles lignes du tableau qui affiche les parties."""
        for widget in self._widgets:
            self.ids.table.remove_widget(widget)
        n = 0
        for game in result:
            n += 1
            nbPlayers = str(self.numberOfPlayers(game=game))
            winner = self.winner(game=game)
            finishTime = str(self.finishTime(game=game, player=winner)).split(".")
            worldName = self.worldName(game=game)
            date = self.gameDate(game=game)
            b = BoxLayout(orientation="horizontal", size_hint=(None, None), size=self.ids.entete.size)  # Récupération de la taille de l'entête, sinon par défaut la taille serait celle de la fenêtre entière
            b.add_widget(
                Label(
                    text=str(n),
                    color=(0, 0, 0, 1),
                    bold=True,
                    size_hint=(0.1, 1),
                    halign="left",
                )
            )
            b.add_widget(
                Label(
                    text=worldName,
                    color=(0, 0, 0, 1),
                    size_hint=(0.18, 1),
                    halign="left",
                )
            )
            b.add_widget(
                Label(
                    text=winner, color=(0, 0, 0, 1), size_hint=(0.18, 1), halign="left"
                )
            )
            b.add_widget(
                Label(
                    text=finishTime[0]+"."+finishTime[1][:2],
                    color=(0, 0, 0, 1),
                    size_hint=(0.18, 1),
                    halign="left",
                )
            )
            b.add_widget(
                Label(
                    text=nbPlayers,
                    color=(0, 0, 0, 1),
                    size_hint=(0.18, 1),
                    halign="left",
                )
            )
            b.add_widget(
                Label(text=date, color=(0, 0, 0, 1), size_hint=(0.18, 1), halign="left")
            )
            self.ids.table.add_widget(b)
            self._widgets.append(b)
        print(n)
    def generateWorldsList(self) -> list:
        """Génère la liste des curcuits jouables"""
        l = list(world[:-5] for world in listdir("client/worlds"))
        l.append("All Worlds")
        return l

    def numberOfPlayers(self, game: dict) -> int:
        """Retourne le nombre de joueurs qui ont joué la partie."""
        return len(game["players"])

    def winner(self, game: dict) -> str:
        """Retourne le nom du vainqueur de la partie."""
        minTime = min(player["finishTime"] for player in game["players"])
        return list(
            player["username"]
            for player in game["players"]
            if player["finishTime"] == minTime
        )[0]

    def finishTime(self, game: dict, player: str) -> float:
        """Retourne le temps qu'a pris le joueur pour finir le circuit, ou False s'il ne l'a pas fini."""
        return list(
            player["finishTime"]
            for player in game["players"]
            if player["username"] == "4444"
        )[0]

    def worldName(self, game: dict) -> str:
        """Retourne le nom du circuit de la partie."""
        return game["world_name"]

    def gameDate(self, game: dict) -> str:
        """Retourne la data et l'heure à laquelle a été jouée la partie."""
        date = game["startDateTime"]
        return str(
            datetime.strptime(date[2:], "%d-%m-%y %H:%M:%S") + timedelta(hours=2)
        )
