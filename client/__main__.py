from os import path
import time
import os.path
from typing import List

import game

dataUrl = path.join("client", "circle.json")
print(f"GameData: {dataUrl}")
eventsList = list()


def output(objects: List[game.objects.Object]):
    for object in objects:
        print(f"Object {object.formID()}:")
        print(f"\tCenter: {object.center()}")
        print(f"\tAngle: {object.angle()}")
    print()


theGame = game.Game(dataUrl, eventsList, output)

print("Starting ...")
for i in range(4):
    theGame.nextFrame(1 / 2)
    # time.sleep(1 / 60)
print("Finisched!")
