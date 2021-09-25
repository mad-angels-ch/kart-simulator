import os
import os.path as path
import configparser

activeDir = os.getcwd()
os.chdir(path.abspath(__file__[:-11]))


import lib

import interfaces
import core
import modules


os.chdir(activeDir)


class LGE:
    _path = os.path.abspath(__file__[:-11])
    _config = configparser.ConfigParser()

    _interfaces = interfaces.Interface()

    _game: core.Game
    _menu: core.Menu

    _graphics: modules.Graphics
    _io: modules.IO
    _physics: modules.Physics

    def __init__(self, configFile: str = None) -> None:
        self._config.read(path.join(self._path, "default.ini"))
        if configFile:
            self._config.read(configFile, "UTF8")

        self._graphics = modules.Graphics(self._config["graphics"], self._interfaces)
        self._io = modules.IO(self._config["io"], self._interfaces)
        self._physics = modules.Physics(self._config["physics"], self._interfaces)

    def run(self) -> None:
        pass
