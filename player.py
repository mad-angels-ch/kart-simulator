from logging import error
import sys
from typing import Tuple
import requests, pickle
import click

from socketio import Client, ClientNamespace


class MultiplayerGame(ClientNamespace):
    def __init__(self, namespace, create, join):
        super().__init__(namespace)
        self.create = create
        self.join = join

    def created(self, error: "None | str" = None):
        if error:
            click.echo(error)
            raise click.Abort()
        input("[Hit enter to start the game]\n")
        self.emit("start")

    def joined(self, error: "None | str" = None):
        if error:
            click.echo(error)
            raise click.Abort()

    def on_connect(self):
        click.echo("Connected!")
        worldVersion_id = None
        if self.create:
            name, worldVersion_id = self.create
        elif self.join:
            name = self.join
        else:
            action = click.prompt(
                "Do you want to [c]reate or [j]oin a game?",
                "j",
                type=click.Choice(["c", "j"]),
                show_choices=False,
                show_default=False,
            )
            name = click.prompt("Name of the game", type=str)
            if action == "c":
                worldVersion_id = str(
                    click.prompt("worldVersion_id of the world to be used", type=int)
                )

        if worldVersion_id == None:
            self.emit(
                "join",
                name,
                callback=self.joined,
            )
        else:
            self.emit(
                "create",
                (name, worldVersion_id),
                callback=self.created,
            )

    def on_game_jsons(self, gameJSONs: Tuple[int]):
        click.echo(f"game_jsons: {gameJSONs}")

    def on_objects_update(self, outputs):
        click.echo(f"objects_update: {outputs}")

    def on_disconnect(self):
        click.echo("Disconnected!")


@click.command()
@click.option(
    "--create",
    type=(str, int),
    help="Use this option if you want to create a game, e.g: 'python player.py --create TestGame 56'",
)
@click.option(
    "--join",
    type=str,
    help="Use this option if you want to join a game, e.g: 'python player.py --join TestGame'",
)
def main(create, join):
    """Create a player to test the ks multiplayer"""
    sio = Client(logger=True, engineio_logger=True)
    sio.register_namespace(MultiplayerGame("/kartmultiplayer", create, join))
    try:
        sio.connect("http://localhost:5000", namespaces="/kartmultiplayer")
    except BaseException as e:
        click.echo(e)
        sys.exit()


if __name__ == "__main__":
    main()
