from typing import List
from kivy.graphics import Ellipse, Color
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from game.events.Event import Object
from client import io_objects
import lib
from kivy.properties import ListProperty
from lib.Point import Point


class IO_Circle(Ellipse):
    _w: Widget
    _scale: float
    _LGECircle: "io_objects.Circle"

    def __init__(
        self,
        widget: Widget,
        LGEObject: "io_objects.Circle",
        source: "str | None" = None):
        """Crée le cercle à ajouter au canvas et prépare son ajout"""
        self._w = widget
        self._LGECircle = LGEObject
        self._radius = self._LGECircle.radius()
        self.lastPos = lib.Point((0, 0))
        
        with self._w.canvas:
            if source:
                Color(rgba=(1,1,1,1))
            else:
                Color(rgba=get_color_from_hex(self._LGECircle.fill().value()))
        Ellipse.__init__(self, source=source, size=(2 * self._radius, 2 * self._radius))

        self.updatePosition()

    def updatePosition(self):
        """Met à jour la position des cercles"""
        if self._LGECircle.center() != self.lastPos:
            self.lastPos = lib.Point(self._LGECircle.center())
            self.pos = self.get_position(
                self._LGECircle.center()
            )

    def get_position(self, center: lib.Point) -> lib.Point:
        """Retourne la position du sommet en bas à gauche du rectangle circonscrit au cercle 
        à partir de son centre"""
        centerVector = lib.Vector((center[0], center[1]))
        position = centerVector - lib.Vector((self._radius, self._radius))
        return lib.Point((position[0], position[1]))
