import configparser
import threading

import interfaces

class IO(threading.Thread):
    _config: configparser.SectionProxy
    _interface: interfaces.Interface

    def __init__(self, config: configparser.SectionProxy, interface: interfaces.Interface) -> None:
        super().__init__()
        self._config = config
        self._interface = interface

    def run(self) -> None:
        print("IO started")
        while True:
            request = self._interface.io.requests.get(block=True)

            if request == "_quit_":
                print("IO stopped")
                break