from typing import List
from kivy.graphics import Mesh, Rectangle, PushMatrix,Rotate, PopMatrix, Color
from typing import List
import math
from client import io_objects
from kivy.uix.widget import Widget
import lib
from logging import warning

class IO_FilledQuadrilateral(Rectangle):
    _scale: float
    _LGEFilledQuadrilateral: "io_objects.IO_FilledQuadrilateral"
    def __init__(self, LGEObject: "io_objects.IO_FilledQuadrilateral", source: str = None, scale=1, translate1: lib.Vector = lib.Vector((0,0)), translate2: lib.Vector = lib.Vector((0,0))):
        """Crée le rectangle à ajouter au canvas et prépare son ajout"""

        self._scale = scale
        self._LGEFilledQuadrilateral = LGEObject
        self._source = source
        self._translation1 = translate1
        self._translation2 = translate2
        self._verticesBR = self._LGEFilledQuadrilateral.verticesBeforeRotation()
        _angle = self._LGEFilledQuadrilateral.angle()*180/math.pi
        
        
        center = self.get_center(self._LGEFilledQuadrilateral.center())
        self._size = (self.get_sizeFromVertices()[0] / self._scale, self.get_sizeFromVertices()[1] / self._scale)
        position = self.get_position(center)
    
        PushMatrix()
        Rotate(origin=center, angle=_angle)
        Rectangle.__init__(self,source=self._source,pos=position,size=self._size)
        PopMatrix()
    
    def updatePosition(self):
        pass
    
    def get_sizeFromVertices(self) -> tuple:
        """Calcule et retourne la taille horizontale et verticale du rectangle avant l'homotétie 
        à partir de ses sommets avant la rotation"""
        size_x = max(self.get_abscissasAndOrdinates()[0])-min(self.get_abscissasAndOrdinates()[0])
        size_y = max(self.get_abscissasAndOrdinates()[1])-min(self.get_abscissasAndOrdinates()[1])
        return (size_x,size_y)
    
    def get_abscissasAndOrdinates(self):
        """Retourne la liste des abscisses et ordonnées du rectangle avant la rotation"""
        return ([point[0] for point in self._verticesBR],[point[1] for point in self._verticesBR])
    
    def get_center(self, centerBefore: lib.Point) -> lib.Point:
        """Calcule et retourne la position visuelle du centre du rectangle 
        à partir des coordonnées de son centre avant les translations et l'homotétie de centre (0;0)"""
        centerTranslated = lib.Point((centerBefore[0],centerBefore[1]))
        centerTranslated.translate(self._translation1)
        centerScaledAndTranslated = lib.Vector((centerTranslated[0],centerTranslated[1])) / self._scale
        center = lib.Point((centerScaledAndTranslated[0], centerScaledAndTranslated[1]))
        center.translate(self._translation2)
        return center
    
    def get_position(self,center: lib.Point) -> lib.Point:
        """Calcule et retourne la position du sommet en bas à gauche du rectangle 
        à partir de son centre"""
        centerVector = lib.Vector((center[0],center[1]))
        position = (centerVector - lib.Vector((self._size[0],self._size[1]))/2)
        return lib.Point((position[0],position[1]))