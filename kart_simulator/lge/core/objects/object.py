from lib.point import Point
from lib.vector import Vector

class Object():
    _name: str = None
    _formID: int

    _center: Point = Point
    _angle: float = 0

    def get_formID(self) -> int:
        return self._formID

    def get_name(self) -> str:
        return self._name