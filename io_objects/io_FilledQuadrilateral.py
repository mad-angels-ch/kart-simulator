from typing import List
from kivy.graphics import Mesh, Rectangle, PushMatrix,Rotate, PopMatrix, Color
from typing import List
import math
import lib

class IO_FilledQuadrilateral(Rectangle):
    def __init__(self, summitsBeforeRotation, source: str, angle = 0):

        self._source = source
        self._vertices = summitsBeforeRotation
        self._angle = angle*180/math.pi
        self.get_posFromVertices()
        self.get_sizeFromVertices()
        
        
        self.pos_x, self.pos_y = self.get_posFromVertices()
        self.size_x, self.size_y = self.get_sizeFromVertices()
        self.center = self.get_center()
        
        
        PushMatrix()
        Rotate(origin=(self.center[0],self.center[1]), angle=self.angle())
        Rectangle.__init__(self,source=self.source(),pos=(self.pos_x,self.pos_y),size=(self.size_x,self.size_y))
        PopMatrix()
        
    def get_abscissasAndOrdinates(self):
        return ([point[0] for point in self.vertices],[point[1] for point in self.vertices])

    def get_posFromVertices(self):
        return (min(self.get_abscissasAndOrdinates()[0]),min(self.get_abscissasAndOrdinates()[1]))
    
    def get_sizeFromVertices(self):
        size_x = max(self.get_abscissasAndOrdinates()[0])-min(self.get_abscissasAndOrdinates()[0])
        size_y = max(self.get_abscissasAndOrdinates()[1])-min(self.get_abscissasAndOrdinates()[1])
        return (size_x,size_y)
    
    def get_center(self):
        center_x = self.pos_x + self.size_x/2
        center_y = self.pos_y + self.size_y/2
        return lib.Point((center_x, center_y))
    
    def updatePosition(self, newPos: list = None):
        pass

    def source(self):
        return self._source

    def angle(self):
        return self._angle