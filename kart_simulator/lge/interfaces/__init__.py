from interfaces.core import CoreInterface
from interfaces.graphics import GraphicsInterface
from interfaces.io import IOInterface
from interfaces.physics import PhysicsInterface

class Interface:
    core = CoreInterface()
    graphics = GraphicsInterface()
    io = IOInterface()
    physics = PhysicsInterface()