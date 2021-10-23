from .Object import Object


class Circle(Object):
    _radius: float

    def __init__(self) -> None:
        super().__init__()
        self._radius = 0

    def radius(self) -> float:
        return self._radius

    def collides(self, object: "Object") -> bool:
        if isinstance(object, Circle):
            return (
                self.center().distanceOf(object.center())
                < self.radius() + object.radius()
            )
        else:
            return object.collides(self)
