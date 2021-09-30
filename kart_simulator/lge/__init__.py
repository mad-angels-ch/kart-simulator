import os
import os.path as path
import configparser

activeDir = os.getcwd()
os.chdir(path.abspath(__file__[:-11]))


from core.core import Core as LGE


os.chdir(activeDir)


# class LGE:
#     _path = os.path.abspath(__file__[:-11])
#     _config = configparser.ConfigParser()
#     _interfaces = interfaces.Interface()

#     _core: core.Core
#     _graphics: modules.Graphics
#     _io: modules.IO
#     _physics: modules.Physics

#     def __init__(self, configFile: str = None) -> None:
#         self._config.read(path.join(self._path, "default.ini"))
#         if configFile:
#             self._config.read(configFile, "UTF8")

#         self._core = core.Core(self._config["core"], self._interfaces)
#         if not self._config.getboolean("core", "server"):
#             self._graphics = modules.Graphics(self._config["graphics"], self._interfaces)
#         self._io = modules.IO(self._config["io"], self._interfaces)
#         self._physics = modules.Physics(self._config["physics"], self._interfaces)

#     def run(self) -> None:
#         if not self._config.getboolean("core", "server"):
#             self._graphics.start()
#         self._io.start()
#         self._physics.start()
#         self._core.start()

#         self._interfaces.graphics.requests.put("_quit_", block=True)
#         self._interfaces.io.requests.put("_quit_", block=True)
#         self._interfaces.physics.requests.put("_quit_", block=True)

#         if not self._config.getboolean("core", "server"):
#             self._graphics.join()
#         self._io.join()
#         self._physics.join()