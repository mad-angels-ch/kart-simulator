from typing import List
from kivy.graphics import Mesh, Color
from typing import List
import lib
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
import client
from client import io_objects

class IO_Polygon(Mesh):
    _w: Widget
    _scale: float
    _LGEPolygon: "io_objects.Polygon"
    def __init__(self, widget: Widget, LGEObject: "io_objects.Polygon", scale=1, translate1: lib.Vector = lib.Vector((0,0)), translate2: lib.Vector = lib.Vector((0,0))):
        """Crée le polygone à ajouter au canvas et prépare son ajout"""
        self._w = widget
        self._scale = scale
        self._LGEPolygon = LGEObject
        self._vertices = []
        self._translation1 = translate1
        self._translation2 = translate2

        self.lastPos = []
        
        self._indices = [i for i in range(len(self._LGEPolygon))]
        
        with self._w.canvas:
            Color(rgba=get_color_from_hex(self._LGEPolygon.fill().value()))
            
        self.updatePosition()
        
            
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

    def updatePosition(self):
        if self._LGEPolygon.vertices() != self.lastPos:
            self.lastPos = self._LGEPolygon.vertices()
            i = 0 
            self._vertices = []
            while i < len(self._LGEPolygon):
                self._vertices.append((self._LGEPolygon.vertices()[i][0]  + self._translation1[0]) / self._scale + self._translation2[0])
                self._vertices.append((self._LGEPolygon.vertices()[i][1] + self._translation1[1]) / self._scale + self._translation2[1])
                self._vertices.append(0)
                self._vertices.append(0)
                i += 1
            self.vertices = self._vertices
