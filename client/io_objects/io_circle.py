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
        scale=1,
        translate1: lib.Vector = lib.Vector((0, 0)),
        translate2: lib.Vector = lib.Vector((0, 0)),
    ):
        """Crée le cercle à ajouter au canvas et prépare son ajout"""
        self._w = widget
        self._scale = scale
        self._LGECircle = LGEObject
        self._radius = self._LGECircle.radius() / self._scale
        self._translation1 = translate1
        self._translation2 = translate2
        self.lastPos = lib.Point((0, 0))
        with self._w.canvas:
            Color(rgba=get_color_from_hex(self._LGECircle.fill().value()))

        Ellipse.__init__(self, size=(2 * self._radius, 2 * self._radius))

        self.updatePosition()

    def updatePosition(self):
        if self._LGECircle.center() != self.lastPos:
            self.lastPos = lib.Point(self._LGECircle.center())
            self.pos = self.get_position(
                self.get_center(lib.Point(self._LGECircle.center()))
            )

    def get_center(self, centerBefore: lib.Point) -> lib.Point:
        centerBefore.translate(self._translation1)
        centerScaledAndTranslated = (
            lib.Vector((centerBefore[0], centerBefore[1])) / self._scale
        )
        centerAfter = lib.Point(
            (centerScaledAndTranslated[0], centerScaledAndTranslated[1])
        )
        centerAfter.translate(self._translation2)
        return centerAfter

    def get_position(self, center: lib.Point) -> lib.Point:
        centerVector = lib.Vector((center[0], center[1]))
        position = centerVector - lib.Vector((self._radius, self._radius))
        return lib.Point((position[0], position[1]))
