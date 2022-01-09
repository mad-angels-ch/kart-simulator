from typing import List
from kivy.graphics import Mesh, Rectangle, PushMatrix,Rotate, PopMatrix, Color
from typing import List
import math
import lib

class IO_FilledQuadrilateral(Rectangle):
    def __init__(self, source: str, summitsBeforeRotation = None, width = 0, height = 0, center = None, angle = 0, scale = 1):

        self._source = source
        self._angle = angle*180/math.pi

        if summitsBeforeRotation:
            self._vertices = summitsBeforeRotation
            self.get_posFromVertices()
            self.get_sizeFromVertices()
            
            self.pos_x, self.pos_y = self.get_posFromVertices()[0]/scale, self.get_posFromVertices()[1]/scale 
            self.size_x, self.size_y = self.get_sizeFromVertices()[0]/scale,self.get_sizeFromVertices()[1]/scale
            self.center = (self.get_center()[0]/scale,self.get_center()[1]/scale)

        elif width and height and center:
            self.pos_x, self.pos_y = (center[0]-width/2)/scale, (center[1]-height/2)/scale
            self.size_x, self.size_y = width/scale, height/scale
            self.center = (center[0]/scale, center[1]/scale)


        else:
            raise "Not enough enformations given to create the filled quadrilateral"
        
        PushMatrix()
        Rotate(origin=(self.center[0],self.center[1]), angle=self.angle())
        Rectangle.__init__(self,source=self.source(),pos=(self.pos_x,self.pos_y),size=(self.size_x,self.size_y))
        # Rectangle.__init__(self,pos=(self.pos_x,self.pos_y),size=(self.size_x,self.size_y))
        PopMatrix()
        
    def get_abscissasAndOrdinates(self):
        return ([point[0] for point in self._vertices],[point[1] for point in self._vertices])

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