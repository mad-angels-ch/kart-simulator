from typing import List
from kivy.graphics import Ellipse

from lib.vector import Vector


class IO_Circle(Ellipse):
    def __init__(self, diametre=30, position=[100, 100], vitesse_x=4, vitesse_y=7):


        Ellipse.__init__(
            self,
            pos=(position[0], position[1]),
            size=(diametre, diametre),
        )


    def get_pos_x(self) -> float:
        return self.pos[0]

    def get_pos_y(self) -> float:
        return self.pos[1]

    def radius(self) -> int:
        return self.size[0] / 2

    def diametre(self) -> int:
        return self.size[0]
    
    def updatePosition(self, newPos: List[float] = None, anglularMotion = 0, vectorialMotion = Vector(0,0), deltaTime = 0):
        if newPos:
            self.pos = (newPos[0], newPos[1])