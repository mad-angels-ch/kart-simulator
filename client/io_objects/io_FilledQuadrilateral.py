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
    def __init__(self, LGEObject: "io_objects.IO_FilledQuadrilateral", source: str = None, scale=1, translate: lib.Vector = lib.Vector((0,0))):
        self._scale = scale
        self._LGEFilledQuadrilateral = LGEObject
        self._source = source
        self._translate = translate
        self._verticesBR = self._LGEFilledQuadrilateral.verticesBeforeRotation()
        _angle = self._LGEFilledQuadrilateral.angle()*180/math.pi
        
        
        center1 = lib.Vector((self._LGEFilledQuadrilateral.center()[0],self._LGEFilledQuadrilateral.center()[1])) / self._scale
        _size1 = (self.get_sizeFromVertices()[0] / self._scale, self.get_sizeFromVertices()[1] / self._scale)
        position1 = center1 - (lib.Vector(_size1)/2)
        
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
        size_x = max(self.get_abscissasAndOrdinates()[0])-min(self.get_abscissasAndOrdinates()[0])
        size_y = max(self.get_abscissasAndOrdinates()[1])-min(self.get_abscissasAndOrdinates()[1])
        return (size_x,size_y)
    
    def get_abscissasAndOrdinates(self):
        return ([point[0] for point in self._verticesBR],[point[1] for point in self._verticesBR])
    
    def get_center(self, centerBefore: lib.Point) -> lib.Point:
        centerScaled = lib.Vector((centerBefore[0],centerBefore[1])) / self._scale
        centerScaledAndTranslated = lib.Point((centerScaled[0],centerScaled[1]))
        centerScaledAndTranslated.translate(self._translate)
        return centerScaledAndTranslated
    
    def get_position(self,center: lib.Point) -> lib.Point:
        centerVector = lib.Vector((center[0],center[1]))
        position = (centerVector - lib.Vector((self._size[0],self._size[1]))/2)
        return lib.Point((position[0],position[1]))