from typing import List
from kivy.graphics import Mesh
from typing import List


class IO_Polygon(Mesh):
    def __init__(self,summits, couleur = '#000000'):

        self.color = couleur

        self._vertices = list()

        self._indices = list()
        self._step = int()
        i = 0
        j = 0
        while i < len(summits):
            self._vertices.append(summits[i][0])
            self._vertices.append(summits[i][1])
            self._vertices.append(0)
            self._vertices.append(0)
            self._step += 1
            self._indices.append(j)
            i += 1
            j += 1
        Mesh.__init__(self,mode = 'triangle_fan',vertices=self._vertices, indices=self._indices)


    def get_vertices(self):
        return self._vertices

    def updatePosition(self, newPos: List[float] = None):
        if newPos:
            newVertices = list()

            for vertex in newPos:
                newVertices.append(vertex[0])
                newVertices.append(vertex[1])
                newVertices.append(0)
                newVertices.append(0)
            
            self._vertices = newVertices
            self.vertices = self._vertices


