import configparser
import threading

import interfaces

class Physics(threading.Thread):
    _config: configparser.SectionProxy
    _interface: interfaces.Interface

    def __init__(self, config: configparser.SectionProxy, interface: interfaces.Interface) -> None:
        super().__init__()
        self._config = config
        self._interface = interface

    def run(self) -> None:
        print("Physics started")
        while True:
            request = self._interface.physics.requests.get(block=True)

            if request == "_quit_":
                print("Physics stopped")
                break