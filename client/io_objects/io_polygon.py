from typing import List
from kivy.graphics import Mesh, Color
from typing import List

from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
import client
from client import io_objects

class IO_Polygon(Mesh):
    _w: Widget
    _scale: float
    _LGEPolygon: "io_objects.Polygon"
    def __init__(self, widget: Widget, LGEObject: "io_objects.Polygon", scale=1):
        """Crée le polygone à ajouter au canvas et prépare son ajout"""
        self._w = widget
        self._scale = scale
        self._LGEPolygon = LGEObject
        self._vertices = []

        self._indices = [i for i in range(len(self._LGEPolygon))]
        i = 0
        with self._w.canvas:
            Color(rgba=get_color_from_hex(self._LGEPolygon.fill().value()))
        while i < len(self._LGEPolygon):
            self._vertices.append(self._LGEPolygon.vertices()[i][0] / self._scale)
            self._vertices.append(self._LGEPolygon.vertices()[i][1] / self._scale)
            self._vertices.append(0)
            self._vertices.append(0)
        #     self._step += 1
        #     self._indices.append(j)
            i += 1
        #     j += 1
        # En raison d'une mauvaise gestion des polygones non-convexes par kivy, 
        # nous sommes pour l'instant contraints de recourir à cette méthode pour afficher ceux-ci 
        # (les polygones non-convexes utilisés ont tous plus de 4 côtés):
        if len(self._vertices) > 16:
            Mesh.__init__(
                self, mode="line_loop", vertices=self._vertices, indices=self._indices
            )
        else:
            Mesh.__init__(
                self,
                mode="triangle_fan",
                vertices=self._vertices,
                indices=self._indices,
            )

    def get_vertices(self):
        return self._vertices

    def updatePosition(self, newPos: List[float] = None):
        if newPos:
            newVertices = list()

            for vertex in newPos:
                newVertices.append(vertex[0])
                newVertices.append(vertex[1])
                newVertices.append(0)
                newVertices.append(0)

            self._vertices = newVertices
            self.vertices = self._vertices
