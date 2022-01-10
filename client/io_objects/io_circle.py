from typing import List
from kivy.graphics import Ellipse, Color
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from game.events.Event import Object
from client import io_objects


import lib

from kivy.properties import ListProperty

class IO_Circle(Ellipse):
    _w: Widget
    _scale: float
    _LGECircle: "io_objects.Circle"
    

    def __init__(self, widget: Widget, LGEObject: "io_objects.Circle", scale = 1):
        """Crée le cercle à ajouter au canvas et prépare son ajout"""
        self._w = widget
        self._scale = scale
        self._LGECircle = LGEObject
        self._radius = self._LGECircle.radius()/self._scale
        
        with self._w.canvas:
            Color(rgba=get_color_from_hex(self._LGECircle.fill().value()))
        center = lib.Vector((self._LGECircle.center()[0],self._LGECircle.center()[1]))/self._scale
        position = center - lib.Vector((self._radius,self._radius))
        Ellipse.__init__(self,pos=position,size=(2*self._radius,2*self._radius))

    def radius(self):
        return self._radius
    def updatePosition(self, newPos: List[float] = None):
        if newPos:
            self.pos = (newPos[0] - self.radius(), newPos[1] - self.radius())
