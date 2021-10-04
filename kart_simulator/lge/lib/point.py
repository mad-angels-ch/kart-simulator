class Point:
    _x: float
    _y: float

    def createFromVector(vector):
        return Point(vector.x(), vector.y())

    def __init__(self, x: float = 0, y: float = 0) -> None:
        self._x = x
        self._y = y

    def x(self) -> float:
        return self._x

    def y(self) -> float:
        return self._y

    def get_x(self) -> float:
        return self._x

    def get_y(self) -> float:
        return self._y

    def __iter__(self):
        return PointIterator(self)


class PointIterator:
    def __init__(self, point: Point) -> None:
        self._point = point
        self._index = 0

    def __next__(self) -> float:
        if self._index == 0:
            self._index += 1
            return self._point.get_x()
        elif self._index == 1:
            self._index += 1
            return self._point.get_y()
        raise StopIteration
