import configparser


class Physics:
    _config: configparser.SectionProxy
    _core: object

    def __init__(self, config: configparser.SectionProxy, core) -> None:
        self._config = config
        self._core = core