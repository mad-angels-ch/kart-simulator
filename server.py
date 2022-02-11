import sys
from typing import Dict, List, Tuple
import requests
import socketio
import time

import game
import lib


class Output:
    _lastStates: Dict[int, Tuple[lib.Point, float]]
    _ping: "function"

    def __init__(self, ping: "function") -> None:
        self._ping = ping
        self._lastStates = {}

    def __call__(self, objects: List[game.objects.Object]) -> None:
        changes = {}
        for obj in objects:
            last = self._lastStates.get(obj.formID())
            if not last or obj.center() != last[0] or obj.angle() != last[1]:
                self._lastStates[obj.formID()] = obj.center(), obj.angle()
                changes[obj.formID()] = (
                    obj.center().x(),
                    obj.center().y(),
                ), obj.angle()
        if changes:
            self._ping(changes)


def createGame(sio: socketio.Client, world_id: int) -> None:
    with open("data.json", "w", encoding="utf8") as f:
        f.write(
            requests.get(
                f"https://lj44.ch/creator/kart/worlds/{world_id}/fabric", timeout=1
            ).text
        )

    def ping(changes: Dict):
        sio.emit("movements", changes)

    with open("data.json", "r", encoding="utf8") as f:
        g = game.Game(f.read(), Output(ping))
    deltaTime = 1 / 60
    while True:
        time.sleep(deltaTime)
        g.nextFrame(deltaTime, [])


if __name__ == "__main__":
    sio = socketio.Client()
    world_id = 19

    def printRoomAndStart(gameID: int) -> None:
        print("Room:", gameID)
        createGame(sio, world_id)
        sys.exit(0)

    @sio.event
    def connect():
        print("I'm connected!")

    @sio.event
    def connect_error(data):
        print("The connection failed!")

    @sio.event
    def disconnect():
        print("I'm disconnected!")

    @sio.event
    def movements(changes: List) -> None:
        print(changes)

    sio.connect("http://localhost:5000")
    sio.emit("new_game", world_id, callback=printRoomAndStart)
