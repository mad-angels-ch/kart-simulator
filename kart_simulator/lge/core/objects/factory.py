from lib.point import Point

from core.objects.circle import Object
from core.objects.circle import Circle


class Factory:
    objectsCreatedCount = 0

    def __call__(
        self, type: str, name: str = None, center: Point = Point(0, 0), angle: float = 0
    ) -> Object:
        if type == "circle":
            newObject = Circle()
        else:
            raise ValueError(f"{type} is not a valid type!")

        newObject._name = name
        newObject._formID = Factory.objectsCreatedCount
        newObject._center = center
        newObject._angle = angle

        Factory.objectsCreatedCount += 1
        return newObject