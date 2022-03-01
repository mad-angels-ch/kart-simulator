from logging import error
import sys
from typing import Tuple
import requests, pickle

from socketio import Client, ClientNamespace


class MultiplayerGame(ClientNamespace):
    def on_connect(self):
        print("Connected!")
        self.emit(
            "join",
            "test",
            callback=lambda error=None: print(error),
        )

    def on_game_jsons(self, gameJSONs: Tuple[int]):
        print("game_jsons:", gameJSONs)
        if not started:
            self.emit("start")

    def on_objects_update(self, outputs):
        print("objects_update:", outputs)

    def on_disconnect(self):
        print("Disconnected!")


if __name__ == "__main__":
    started = False
    sio = Client()
    sio.register_namespace(MultiplayerGame("/kartmultiplayer"))

    sio.connect("http://localhost:5000", namespaces="/kartmultiplayer")
