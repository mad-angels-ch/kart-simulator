from kivy.graphics import Rectangle





class Kart(Rectangle):
    def __init__(self, x1 = 100, y1 = 100, largeur = 25, hauteur = 20, angle = 0):
        Rectangle.__init__(self, pos=(x1, y1), size=(largeur, hauteur))

        self.angle = angle
        self.speed_x = 0
        self.speed_y = 0


    def get_pos_x(self) -> float:
        return self.pos[0]

    def get_pos_y(self) -> float:
        return self.pos[1]

    def width(self) -> int:
        return self.size[0]

    def height(self) -> int:
        return self.size[1]

    def changePos(self) -> None:
        self.pos = (self.get_pos_x() + self.speed_x, self.get_pos_y() + self.speed_y)
    
    def changeSpeedX(self, speedX):
        self.speed_x = speedX

    def changeSpeedY(self, speedY):
        self.speed_y = speedY
