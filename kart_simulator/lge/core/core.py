import configparser
import os
import threading
import time

import lib.tests
import core.objects as objects
import modules


class Core(threading.Thread):
    _path = os.path.abspath("")
    config: configparser.SectionProxy

    events = object()

    objects = objects.Container()

    graphics: modules.Graphics
    io: modules.IO
    physics: modules.Physics

    _requestStop = False

    def __init__(self, configPath: str = None) -> None:
        super().__init__()
        config = configparser.ConfigParser()
        config.read(os.path.join(self._path, "default.ini"))
        if configPath:
            config.read(configPath)

        self.config = config["core"]
        self.graphics = modules.Graphics(config["graphics"], self)
        self.io = modules.IO(config["io"], self)
        self.physics = modules.Physics(config["physics"], self)

        if self.config.getboolean("tests"):
            self._tests()

    def run(self) -> None:
        self.io.run(self._startGame)

    def _tests(self) -> None:
        lib.tests.run()

    def _startGame(self) -> None:
        self._mainLoop()

    def _startMainMenu(self) -> None:
        pass

    def stop(self) -> None:
        self._requestStop = True

    def resume(self) -> None:
        pass

    def restart(self) -> None:
        self._startGame()

    def _mainLoop(self) -> None:
        while not self._requestStop:
            # récupéré les inputs

            
            # lancer physics


            # lancer events


            # lancer graphics


            # attendre la frame suivante
            time.sleep(1/60)