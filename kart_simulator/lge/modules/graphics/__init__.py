import configparser

import interfaces

class Graphics:
    _config: configparser.SectionProxy
    _interface: interfaces.Interface()

    def __init__(self, config: configparser.SectionProxy, interface: interfaces.Interface) -> None:
        self._config = config
        self._interface = interface