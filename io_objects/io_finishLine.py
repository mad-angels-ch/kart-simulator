from kivy.graphics import Rectangle




class IO_FinishLine(Rectangle):
    def __init__(self):
        self.color = "repeatPattern"
        Rectangle.__init__(self,source = "client/Images/finish_line.jpg",pos=(0,100), size=(25,100))
    
    def get_pos(self):
        return self.pos
    
    def get_size(self):
        return self.size
    
    def updatePosition(self, newPos: list = None):
        pass