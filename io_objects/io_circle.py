from kivy.graphics import Ellipse


class IO_Circle(Ellipse):
    def __init__(self, diametre=30, position=[100, 100], vitesse_x=4, vitesse_y=7):


        Ellipse.__init__(
            self,
            pos=(position[0], position[1]),
            size=(diametre, diametre),
        )


    def get_pos_x(self) -> float:
        return self.position[0]

    def get_pos_y(self) -> float:
        return self.position[1]

    def radius(self) -> int:
        return self.size[0] / 2

    def diametre(self) -> int:
        return self.size[0]
    
    def updatePosition(self,newPos: list[float,float] = None):
        if newPos:
            self.position = (self.get_pos_x() + newPos[0], self.get_pos_y() + newPos[1])