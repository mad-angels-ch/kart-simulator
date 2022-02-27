from logging import error
import sys
import requests, pickle

from socketio import Client, ClientNamespace


class MultiplayerGame(ClientNamespace):
    def on_connect(self):
        print("Connected!")

    def on_disconnect(self):
        print("Disconnected!")

    def on_update(self, json):
        print(json)


if __name__ == "__main__":
    sio = Client()
    sio.register_namespace(MultiplayerGame("/kartmultiplayer"))
    sio.connect("http://localhost:5000", namespaces="/kartmultiplayer")
