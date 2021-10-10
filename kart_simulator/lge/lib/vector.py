import math
from typing import overload

class Vector:
    _x: float
    _y: float

    # @overload
    def __init__(self, x: float = 0, y: float = 0):
        self._x = x
        self._y = y

    # @overload
    # def __init__(self, vector: "Vector"):
    #     self._x = vector._x
    #     self._y = vector._y

    def __len__(self) -> int:
        return 2

    def __iter__(self):
        return iter((self._x, self._y))

    def __neg__(self) -> "Vector":
        return Vector(-self._x, -self._y)

    def __pos__(self) -> "Vector":
        return self

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self._x + other._x, self._y + other._y)

    def __sub__(self, other: "Vector") -> "Vector":
        return self + (-other)

    # @overload
    def __mul__(self, other: float) -> "Vector":
        return Vector(self._x * other, self._y * other)

    def __truediv__(self, other: float) -> "Vector":
        return Vector(self._x / other, self._y / other)

    def __pow__(self, other: int) -> float:
        if other != 2:
            raise ValueError()
        return self * self

    def __eq__(self, o: "Vector") -> bool:
        return self._x == o._x and self._y == o._y

    def __ne__(self, o: object) -> bool:
        return not self == o

    def __getitem__(self, index: "int | str") -> float:
        if type(index) == str:
            index = index.lower()
        if index == 0 or index == "x":
            return self._x
        elif index == 1 or index == "y":
            return self._y
        else:
            raise ValueError()

    def __setitem__(self, index: "int | str", value: float) -> None:
        if type(index) == str:
            index = index.lower()
        if index == 0 or index == "x":
            self._x = value
        elif index == 1 or index == "y":
            self._y = value
        else:
            raise ValueError()

    def norm(self) -> None:
        return math.hypot(*self)

    def set_norm(self, newNorm: float) -> None:
        newVector = self * (newNorm / self.norm())
        for i in range(len(self)):
            self[i] = newVector[i]

    def scalarProduct(self, other: "Vector") -> float:
        return self._x * other._x + self._y * other._y

    def isNormal(self, other: "Vector") -> bool:
        return self.scalarProduct(other) == 0

    def isCollinear(self, other: "Vector") -> bool:
        if self == Vector(0, 0) or other == Vector(0, 0):
            return True
        return not self.isNormal(other)

    def normalVector(self) -> "Vector":
        return Vector(-self._y, self._x)

    def direction(self) -> float:
        """Retourne l'angle formé par ce vecteur et un vecteur de composantes 1 et 0.
        L'angle est situé entre 0 et 2 Pi"""
        return math.atan2(self._y, self._x)

    def rotate(self, angle: float) -> None:
        cos = math.cos(angle)
        sin = math.sin(angle)
        self._x = self._x * cos - self._y * sin
        self._y = self._x * sin + self._y * cos

    def orthogonalProjection(self, vector: "Vector") -> "Vector":
        "Projete ce vecteur sur le vecteur donné en paramètre"
        return self * (self * vector) / (vector._x ** 2)

    def scaleX(self, factor: float) -> None:
        "Multiplie la composante du vecteur par le facteur donné"
        self._x *= factor

    def scaleY(self, factor: float) -> None:
        "Multiplie la composante du vecteur par le facteur donné"
        self._y *= factor

    def x(self) -> float:
        "Obsolète, utiliser self[0] ou self['x']"
        return self._x

    def y(self) -> float:
        "Obsolète, utiliser self[1] ou self['y']"
        return self._y

    def get_x(self) -> float:
        "Obsolète, utiliser self[0] ou self['x']"
        return self._x

    def get_y(self) -> float:
        "Obsolète, utiliser self[1] ou self['y']"
        return self._y