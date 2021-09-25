import configparser
import time

from core.objects.container import Container as ObjectsContainer

class Game:
    _config = configparser.SectionProxy

    _isClient = False

    _stopRequested = False
    _objectsContainer = ObjectsContainer()

    def __init__(self, coreConfig: configparser.SectionProxy()) -> None:
        self._config = coreConfig

    def start(self) -> None:
        # charger les données

        # lancer IO pour créé la fenêtre de jeu

        # lancer graphics pour afficher le circuit

        self.gameLoop()

    def stop(self) -> None:
        self._stopRequested = True

    def resume(self) -> None:
        pass

    def restart(self) -> None:
        pass

    def gameLoop(self) -> None:
        while not self._stopRequested:
            # récupère les inputs

            #connecté à un serveur ?
            if self._isClient:
                # transmettre les inputs au serveur
                pass

            else:
                # lancer physics
                pass
                
            if self._config.getboolean("server"):
                # transmettre les modifications aux clients
                pass

            else:
                # lancer graphics
                pass

            time.sleep(1/60)


        if self._config.getboolean("server"):
            # détruire la partie
            pass
        else:
            # retourner le contrôle à LGE pour se remettre en mode menu
            pass