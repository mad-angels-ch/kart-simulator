import configparser
import time

import interfaces

from core.game import Game
from core.menu import Menu

import core.objects as objects

class Core:
    _config: configparser.SectionProxy
    _interface: interfaces.Interface

    # _game: Game()
    # _menu: Menu()

    def __init__(self, config: configparser.SectionProxy, interface: interfaces.Interface) -> None:
        self._config = config
        self._interface = interface

    def start(self) -> None:
        if not self._config.getboolean("server"):
            if self._config.getboolean("no_main_menu"):
                time.sleep(1)