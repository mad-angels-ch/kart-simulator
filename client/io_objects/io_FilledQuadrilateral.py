from kivy.graphics.transformation import Matrix
from typing import List
from kivy.graphics import Mesh, Rectangle, PushMatrix, Rotate, PopMatrix, Color, BindTexture
from typing import List
import math
from client import io_objects
from kivy.uix.widget import Widget
import lib
from logging import warning
from kivy.uix.image import Image


class IO_FilledQuadrilateral(Rectangle):
    _scale: float
    _LGEFilledQuadrilateral: "io_objects.IO_FilledQuadrilateral"

    def __init__(
        self,
        LGEObject: "io_objects.IO_FilledQuadrilateral",
        source: str = None,
        patternToRepeat: str = None
    ):
        """Crée le rectangle à ajouter au canvas et prépare son ajout"""

        self._LGEFilledQuadrilateral = LGEObject
        self._verticesBR = self._LGEFilledQuadrilateral.verticesBeforeRotation()
        _angle = self._LGEFilledQuadrilateral.angle() * 180 / math.pi

        self.center =self._LGEFilledQuadrilateral.center()
        self._size = (
            self.get_sizeFromVertices()
        )
        position = self.get_position(self.center)

        if patternToRepeat:
            texture = None
            texture = Image(source=patternToRepeat, allow_stretch = False, keep_ratio = True).texture
            texture.wrap = "repeat"
            texture.uvsize = (self._size[0]//10,self._size[1]//10)
            PushMatrix()
            Rotate(origin=self.center, angle=_angle)
            Rectangle.__init__(self, texture=texture, pos=position, size=self._size)
            PopMatrix()
            

        else:
            PushMatrix()
            Rotate(origin=self.center, angle=_angle)
            Rectangle.__init__(self, source=source, pos=position, size=self._size)
            PopMatrix()

    def updatePosition(self):
        pass

    def get_sizeFromVertices(self) -> tuple:
        """Calcule et retourne la taille horizontale et verticale du rectangle avant l'homotétie
        à partir de ses sommets avant la rotation"""
        size_x = max(self.get_abscissasAndOrdinates()[0]) - min(
            self.get_abscissasAndOrdinates()[0]
        )
        size_y = max(self.get_abscissasAndOrdinates()[1]) - min(
            self.get_abscissasAndOrdinates()[1]
        )
        return (size_x, size_y)

    def get_abscissasAndOrdinates(self):
        """Retourne la liste des abscisses et ordonnées du rectangle avant la rotation"""
        return (
            [point[0] for point in self._verticesBR],
            [point[1] for point in self._verticesBR],
        )

    def get_position(self, center: lib.Point) -> lib.Point:
        """Calcule et retourne la position du sommet en bas à gauche du rectangle
        à partir de son centre"""
        centerVector = lib.Vector((center[0], center[1]))
        position = centerVector - lib.Vector((self._size[0], self._size[1])) / 2
        return lib.Point((position[0], position[1]))
