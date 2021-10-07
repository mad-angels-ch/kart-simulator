import math
from typing import overload

class Vector:
    _x: float
    _y: float

    @overload
    def __init__(self, x: float = 0, y: float = 0):
        self._x = x
        self._y = y

    @overload
    def __init__(self, vector: "Vector"):
        self._x = vector._x
        self._y = vector._y

    def __len__(self) -> int:
        return 2

    def __iter__(self):
        return (self._x, self._y)

    def __neg__(self) -> "Vector":
        return Vector(-self._x, self._y)

    def __pos__(self) -> "Vector":
        return self

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self._x + other._x, self._y + other._y)

    def __iadd__(self, other: "Vector") -> None:
        for i in range(len(self)):
            self[i] = self[i] + other[i]

    def __sub__(self, other: "Vector") -> "Vector":
        return self + (-other)

    def __isub__(self, other: "Vector") -> None:
        for i in range(len(self)):
            self[i] = self[i] - other[i]

    @overload
    def __mul__(self, other: float) -> "Vector":
        return Vector(self._x * other, self._y * other)

    def __imul__(self, other: float) -> None:
        for i in range(len(self)):
            self[i] = self[i] * other[i]

    @overload
    def __mul__(self, other: "Vector") -> float:
        "Retourne le produit scalaire des deux vecteurs"
        return self._x * other._x + self._y * other._y

    def __truediv__(self, other: float) -> "Vector":
        return Vector(self._x / other, self._y / other)

    def __idiv__(self, other: float) -> None:
        for i in range(len(self)):
            self[i] = self[i] / other[i]

    def __pow__(self, other: int) -> float:
        if other != 2:
            raise ValueError()
        return self * self

    def __eq__(self, o: "Vector") -> bool:
        return self._x == o._x and self._y == o._y

    def __ne__(self, o: object) -> bool:
        return not self == o

    @overload
    def __getitem__(self, index: int) -> float:
        if index == 0:
            return self._x
        elif index == 1:
            return self._y
        else:
            raise ValueError()

    @overload
    def __getitem__(self, index: str) -> float:
        if index.lower() == "x":
            return self._x
        elif index.lower() == "y":
            return self._y
        else:
            raise ValueError()

    def norm(self) -> None:
        return math.hypot(self._x, self._y)

    def set_norm(self, newNorm: float) -> None:
        self._x, self._y *= newNorm / self.norm()

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