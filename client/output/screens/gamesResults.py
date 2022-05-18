import json
from datetime import datetime, timedelta
from os import listdir
from typing import List
import webbrowser

from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.metrics import sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

from .layouts import CustomPopup

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
                self.generateTables(result.json())

        elif self.ids.best_games.state == "down":
            if self.ids.username.text:
                chosenOptions["username"] = self.ids.username.text
            result = self.app.session.get(
                self.app.server + "/games/kart/bestgames.json", params=chosenOptions
            )
            if result.status_code == 400:
                pass
            else:
                self.generateTables(result.json())

    def generateTables(self, result: List[dict]) -> None:
        """Génère les nouvelles lignes du tableau qui affiche les parties."""
        for widget in self._widgets:
            self.ids.table.remove_widget(widget)
        self._widgets = []
        n = 0
        for game in result:
            n += 1
            nbPlayers = str(self.numberOfPlayers(game=game))
            winner = self.winner(game=game)
            finishTime = str(self.finishTime(game=game, player=winner)).split(".")
            worldName = self.worldName(game=game)
            date = self.gameDate(game=game)
            b = BoxLayout(
                orientation="horizontal",
                size_hint=(None, None),
                size=self.ids.entete.size,
            )  # Récupération de la taille de l'entête, sinon par défaut la taille serait celle de la fenêtre entière
            if self.ids.my_games.state == "down":
                if self.hasBurned(
                    game=game, player=self.app.get_userSettings()["username"]
                ):
                    with b.canvas.before:
                        Color(1, 0, 0, 1)
                        Rectangle(size=b.size, pos=(0, (len(result) - n) * 50))
                else:
                    with b.canvas.before:
                        Color(0, 1, 0, 1)
                        Rectangle(size=b.size, pos=(0, (len(result) - n) * 50))
            elif self.ids.best_games.state == "down":
                with b.canvas.before:
                    Color(0, 0, 1, 0.1)
                    Rectangle(size=b.size, pos=(0, (len(result) - n) * 50))

            b.add_widget(
                Label(
                    text=str(n),
                    font_size=sp(20),
                    color=(0, 0, 0, 1),
                    bold=True,
                    size_hint=(0.1, 1),
                    halign="left",
                )
            )
            for name in [
                worldName,
                winner,
                finishTime[0] + "." + finishTime[1][:2],
                nbPlayers,
                date,
            ]:
                b.add_widget(
                    Label(
                        text=name,
                        font_size=sp(20),
                        color=(0, 0, 0, 1),
                        size_hint=(0.18, 1),
                        halign="left",
                    )
                )
            self.ids.table.add_widget(b)
            self._widgets.append(b)

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
        try:
            minTime = min(
                player["finishTime"]
                for player in game["players"]
                if player["completed"] == 1
            )
        except ValueError:
            return "No Winner"
        else:
            return list(
                player["username"]
                for player in game["players"]
                if player["finishTime"] == minTime
            )[0]

    def finishTime(self, game: dict, player: str) -> float:
        """Retourne le temps qu'a pris le joueur pour finir le circuit, ou False s'il ne l'a pas fini."""
        if player == "No Winner":
            return 0.00
        else:
            return list(
                p["finishTime"] for p in game["players"] if p["username"] == player
            )[0]

    def worldName(self, game: dict) -> str:
        """Retourne le nom du circuit de la partie."""
        return game["world_name"]

    def gameDate(self, game: dict) -> str:
        """Retourne la data et l'heure à laquelle a été jouée la partie."""
        date = game["startDateTime"]
        return str(
            datetime.strptime(date[2:], "%y-%m-%d %H:%M:%S") + timedelta(hours=2)
        )

    def hasBurned(self, game: dict, player: str) -> bool:
        """Retourne False si le joueur spécifié a terminé la course sans se faire brûler."""
        reponse = list(
            p["burned"] for p in game["players"] if p["username"] == player
        )  # Si je faisais bool(p["burned"] for p in game["players"] if p["username"] == player) avec p["burned"] == 0, cela retourne True = bool([0]), et pas bool(0) = False
        return bool(reponse[0])

    def playersList(self, game: dict) -> list:
        """Retourne la liste des joueurs ayant participé à la partie."""
        return list(p["username"] for p in game["players"])

    def SettingsPopup(self) -> None:
        """Ajoute le Popup qui demande à l'utilisateur s'il veut se logger."""
        self.popup = CustomPopup(
            "You must be logged in to use this function.",
            functions={"Log In":self.pushLogIn,"Sign Up":lambda _:webbrowser.open(f"{self.app.server}/auth/register", autoraise=True),"No":lambda _: self.remove_widget(self.popup)}
        )
        self.add_widget(self.popup)

    def pushLogIn(self, button) -> None:
        self.app.manager.push("LogIn")
        self.remove_widget(self.popup)

    def change_state(self) -> None:
        """Décoche le bouton "my games" si le joueur n'est pas connecté."""
        self.ids.my_games.state = "normal"
