import configparser
from typing import Any, Iterable, Mapping


class IO:
    _config: configparser.SectionProxy
    _core: object

    def __init__(self, config: configparser.SectionProxy, core) -> None:
        self._config = config
        self._core = core

    def run(
        self, callback, *args: Iterable, **kwargs: Mapping[str, Any]
    ) -> None:
        """Lance l'interface puis lance callback une fois prêt"""
        # lance l'interface


        callback(*args, **kwargs)
