from typing import List
from kivy.graphics import Mesh, Rectangle, PushMatrix,Rotate, PopMatrix, Color
from typing import List
import math
from client import io_objects
from kivy.uix.widget import Widget
import lib

class IO_FilledQuadrilateral(Rectangle):
    _scale: float
    _LGEFilledQuadrilateral: "io_objects.IO_FilledQuadrilateral"
    def __init__(self, LGEObject: "io_objects.IO_FilledQuadrilateral", source: str = None, scale=1):
        self._scale = scale
        self._LGEFilledQuadrilateral = LGEObject
        self._source = source
        
        self._verticesBR = self._LGEFilledQuadrilateral.verticesBeforeRotation()
        
        _angle = self._LGEFilledQuadrilateral.angle()*180/math.pi
        center = lib.Vector((self._LGEFilledQuadrilateral.center()[0],self._LGEFilledQuadrilateral.center()[1])) / self._scale
        _size = self.get_sizeFromVertices()
        position = center - lib.Vector(_size)/2
        

        
        PushMatrix()
        Rotate(origin=center, angle=_angle)
        Rectangle.__init__(self,source=self._source,pos=position,size=_size)
        PopMatrix()
    
    def updatePosition(self, newPos: list = None):
        pass
    
    def get_sizeFromVertices(self):
        size_x = max(self.get_abscissasAndOrdinates()[0])-min(self.get_abscissasAndOrdinates()[0])
        size_y = max(self.get_abscissasAndOrdinates()[1])-min(self.get_abscissasAndOrdinates()[1])
        return (size_x,size_y)
    
    def get_abscissasAndOrdinates(self):
        return ([point[0] for point in self._verticesBR],[point[1] for point in self._verticesBR])