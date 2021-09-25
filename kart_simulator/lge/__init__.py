import os
import os.path as path
import configparser

activeDir = os.getcwd()
os.chdir(path.abspath(__file__[:-11]))


import core.states as states


os.chdir(activeDir)


class LGE:
    _path = os.path.abspath(__file__[:-11])
    _config = configparser.ConfigParser()
    _game: states.Game

    def __init__(self, configFile: str = None) -> None:
        self._config.read(path.join(self._path, "default.ini"))
        if configFile:
            self._config.read(configFile, "UTF8")
        self._game = states.Game(self._config["core"])

    def run(self) -> None:
        if self._config.getboolean("core", "server"):
            # il s'agit d'un server
            pass

        else:
            if self._config.getboolean("lge", "main_menu"):
                states.Menu().main()
            else:
                states.Game(self._config["core"]).start()