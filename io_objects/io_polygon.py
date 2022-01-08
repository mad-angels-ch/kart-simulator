from typing import List
from kivy.graphics import Mesh
from typing import List


class IO_Polygon(Mesh):
    def __init__(self, summits, couleur="#000000", scale=1):

        self.color = couleur

        self._vertices = list()

        self._indices = list()
        self._step = int()
        i = 0
        j = 0
        while i < len(summits):
            self._vertices.append(summits[i][0] / scale)
            self._vertices.append(summits[i][1] / scale)
            self._vertices.append(0)
            self._vertices.append(0)
            self._step += 1
            self._indices.append(j)
            i += 1
            j += 1
        # En raison d'une mauvaise gestion des polygones non-convexes par kivy, 
        # nous sommes pour l'instant contraints de recourir à cette méthode pour afficher ceux-ci 
        # (les polygones non-convexes utilisés ont tous plus de 4 côtés):
        if len(self._vertices) > 16:
            Mesh.__init__(
                self, mode="line_loop", vertices=self._vertices, indices=self._indices
            )
        else:
            Mesh.__init__(
                self,
                mode="triangle_fan",
                vertices=self._vertices,
                indices=self._indices,
            )

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
