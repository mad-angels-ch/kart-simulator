from typing import List
from kivy.graphics import Mesh, Color
from typing import List
import lib
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
import client
from client import io_objects
from kivy.uix.image import Image

class IO_Polygon(Mesh):
    _w: Widget
    _scale: float
    _LGEPolygon: "io_objects.Polygon"
    def __init__(self, widget: Widget, LGEObject: "io_objects.Polygon", patternToRepeat: str = None):
        """Crée le polygone à ajouter au canvas et prépare son ajout"""
        self._w = widget
        self._LGEPolygon = LGEObject
        self._vertices = []
        
        texture = None
        if patternToRepeat:
            texture = Image(source=patternToRepeat, allow_stretch = False, keep_ratio = True).texture
            texture.wrap = "repeat"
            texture.uvsize = (100,100)
        
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
                self, texture=texture, mode="line_loop", vertices=self._vertices, indices=self._indices
            )
        else:
            Mesh.__init__(
                self,
                mode="triangle_fan",
                vertices=self._vertices,
                indices=self._indices,
            )

    def updatePosition(self):
        """Calcule et met à jour la position des polygones en fonction de la liste de ses sommets"""
        if self._LGEPolygon.vertices() != self.lastPos:
            self.lastPos = self._LGEPolygon.vertices()
            i = 0 
            self._vertices = []
            while i < len(self._LGEPolygon):
                self._vertices.append(self._LGEPolygon.vertices()[i][0])
                self._vertices.append(self._LGEPolygon.vertices()[i][1])
                self._vertices.append(0)
                self._vertices.append(0)
                i += 1

                
            self.vertices = self._vertices
