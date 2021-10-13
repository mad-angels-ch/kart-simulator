import time

import game

dataUrl = ""
eventsList = list()


def output(objects):
    for object in objects:
        print(f"Object {object}:")
        print(f"Center: {object.center()}")
        print(f"Angle: {object.angle()}")
        print()


theGame = game.Game(dataUrl, eventsList, output)

print("Starting ...")
for i in range(100):
    theGame.nextFrame(1 / 60)
    time.sleep(1 / 60)
print("Finisched!")
