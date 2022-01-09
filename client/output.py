from logging import warning
from typing import Any, Dict, List

from kivy.utils import get_color_from_hex
from kivy.graphics import Color
from kivy.uix.widget import Widget

from game import objects as game_objects
from game.objects import fill as game_fill
from client import io_objects


class OutputFactory:
    _w: Widget
    _createdObject: Dict[int, Any]
    _scale: float
    _initialized: bool

    _gates: List[game_objects.Gate]

    def __init__(self, widget: Widget, scale: float) -> None:
        self._w = widget
        self._createdObject = {}
        self._scale = scale
        self._initialized = False

        self._gates = []

    def createKart(self, obstacle: game_objects.Kart) -> io_objects.FilledQuadrilateral:
        self._w.kart_ID = obstacle.formID()
        with self._w.canvas:
            Color(rgba=(1, 1, 1, 1))
            io_obstacle = io_objects.FilledQuadrilateral(
                height=16,
                width=50,
                center=obstacle.center(),
                source="client/Images/kartInGame.jpg",
                angle=obstacle.angle(),
                scale=self._scale,
            )
        return io_obstacle

    def __call__(self, objects: List[game_objects.Object]) -> None:
        if self._initialized:
            self._w.updateGatesCount(self._gates)

        else:
            # calculer la taille du canvas
            pass

        for obstacle in objects:
            if not self._initialized or obstacle.formID() not in self._createdObject:
                if isinstance(obstacle.fill(), game_fill.Hex):
                    if obstacle:
                        self._w.color = get_color_from_hex(obstacle.fill().value())

                        if isinstance(obstacle, game_objects.Circle):
                            with self._w.canvas:
                                Color(rgba=self._w.color)
                            pos_x = obstacle.center()[0] - obstacle.radius()
                            pos_y = obstacle.center()[1] - obstacle.radius()
                            io_obstacle = io_objects.Circle(
                                diametre=2 * obstacle.radius(),
                                position=[pos_x, pos_y],
                                couleur=obstacle.fill().value(),
                                scale=self._scale,
                            )
                            self._w.canvas.add(io_obstacle)

                        elif isinstance(obstacle, game_objects.Polygon):
                            if isinstance(obstacle, game_objects.Kart):
                                io_obstacle = self.createKart(obstacle)

                            else:
                                with self._w.canvas:
                                    Color(rgba=self._w.color)
                                io_obstacle = io_objects.Polygon(
                                    summits=obstacle.vertices(),
                                    couleur=obstacle.fill().value(),
                                    scale=self._scale,
                                )
                                self._w.canvas.add(io_obstacle)

                elif isinstance(obstacle.fill(), game_fill.Pattern):
                    if len(obstacle) == 4:
                        if isinstance(obstacle, game_objects.FinishLine):
                            with self._w.canvas:
                                io_obstacle = io_objects.FinishLine(
                                    summitsBeforeRotation=obstacle.verticesBeforeRotation(),
                                    angle=obstacle.angle(),
                                    scale=self._scale,
                                )
                        elif isinstance(obstacle, game_objects.Gate):
                            with self._w.canvas:
                                self._gates.append(obstacle)
                                io_obstacle = io_objects.Gates(
                                    summitsBeforeRotation=obstacle.verticesBeforeRotation(),
                                    angle=obstacle.angle(),
                                    scale=self._scale,
                                )
                        else:
                            warning("TO BE IMPLEMENTED")
                            source = obstacle.sourceImage
                            with self._w.canvas:
                                io_obstacle = io_objects.FilledQuadrilateral(
                                    summitsBeforeRotation=obstacle.verticesBeforeRotation(),
                                    source=source,
                                    angle=obstacle.angle(),
                                    scale=self._scale,
                                )
                    else:
                        raise "Only quadrilaterals can be filled with a pattern"

                else:
                    raise "Unsupported color type"

                self._createdObject[obstacle.formID()] = io_obstacle

            else:
                # mettres les positions à jour
                io_object = self._createdObject[obstacle.formID()]
                if isinstance(obstacle, game_objects.Circle):
                    io_object.updatePosition(newPos=obstacle.center())
                elif isinstance(obstacle, game_objects.Kart):
                    self._w.canvas.remove(io_object)
                    self._createdObject[obstacle.formID()] = self.createKart(obstacle)
                elif isinstance(obstacle, game_objects.Polygon):
                    io_object.updatePosition(newPos=obstacle.vertices())
                    if isinstance(obstacle, game_objects.FinishLine):
                        self._w.updateLapsCount(obstacle)

        self._initialized = True
