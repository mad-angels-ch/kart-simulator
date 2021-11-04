from logging import warning

import lib


class AngularMotion:
    _speed: float
    _center: lib.Point

    def __init__(self, speed: float = 0, center=lib.Point((0, 0))) -> None:
        self._speed = speed
        self._center = center

    def updateReferences(self, deltaTime: float) -> None:
        pass

    def center(self) -> lib.Point:
        return self._center

    def rotationCenter(self) -> lib.Point:
        warning(f"{__name__}.rotationCenter() is deprecated, use center() instead.")
        return self.center()

    def set_center(self, newCenter: lib.Point) -> None:
        self._center = newCenter

    def set_rotationCenter(self, newRotationCenter: lib.Point) -> None:
        warning(
            f"{__name__}.set_rotationCenter() is deprecated, use set_center() instead"
        )
        return self.set_center(newRotationCenter)

    def relativeAngle(self, deltaTime: float = 0) -> float:
        return self._speed * deltaTime

    def speed(self, deltaTime: float = 0) -> float:
        return self._speed

    def set_speed(self, newSpeed: float) -> None:
        self._speed = newSpeed

    def speedAtPoint(self, point: lib.Point, deltaTime: float = 0) -> lib.Vector:
        normal = lib.Vector.fromPoints(self.center(), point)
        speed = lib.Vector((0, self.speed(deltaTime) * normal.norm()))
        speed.rotate(normal.direction())
        return speed
