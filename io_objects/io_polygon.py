from kivy.graphics import Mesh



class IO_Polygon(Mesh):
    def __init__(self,*args):


        self.vertices = list()
        self.indices = list()
        self.step = int()
        i = 0
        j = 0
        while i < len(args):
            self.vertices.append(args[i])
            self.vertices.append(args[i+1])
            self.vertices.append(0)
            self.vertices.append(0)
            self.step += 1
            self.indices.append(j)
            i += 2
            j += 1

        Mesh.__init__(self,mode = 'triangle_fan',vertices=self.vertices, indices=self.indices)

