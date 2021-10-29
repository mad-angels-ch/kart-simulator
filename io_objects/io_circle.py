from typing import List
from kivy.graphics import Ellipse
from kivy.utils import get_color_from_hex

from lib.vector import Vector
from kivy.properties import ListProperty

class IO_Circle(Ellipse):


    def __init__(self, diametre=30, position=[100, 100], vitesse_x=4, vitesse_y=7, couleur = '#000000'):


        Ellipse.__init__(
            self,
            pos=(position[0], position[1]),
            size=(diametre, diametre),
        )

        self.color = couleur
        

    def get_pos_x(self) -> float:
        return self.pos[0] + self.radius()

    def get_pos_y(self) -> float:
        return self.pos[1] + self.radius()

    def radius(self) -> int:
        return self.size[0] / 2

    def diametre(self) -> int:
        return self.size[0]
    
    def updatePosition(self, newPos: list[float] = None):
        if newPos:
            self.pos = (newPos[0] - self.radius(), newPos[1] - self.radius())
