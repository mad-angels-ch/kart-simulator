class Vector:
    _x: float
    _y: float

    def __init__(self, x: float = 0, y: float = 0) -> None:
        self._x = x
        self._y = y

    def get_x(self) -> float:
        return self._x

    def get_y(self) -> float:
        return self._y

    def __iter__(self):
        return VectorIterator(self)


class VectorIterator:
    def __init__(self, vector: Vector) -> None:
        self._vector = vector
        self._index = 0

    def __next__(self) -> float:
        if self._index == 0:
            self._index += 1
            return self._vector.get_x()
        elif self._index == 1:
            self._index += 1
            return self._vector.get_y()
        raise StopIteration
