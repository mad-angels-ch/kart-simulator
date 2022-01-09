from logging import warning
from typing import List

from kivy.utils import get_color_from_hex
from kivy.graphics import Color
from kivy.uix.widget import Widget

from game import objects as game_objects
from game.objects import fill as game_fill
import io_objects

from client.output_game import output

class OutputFactory:
    _w: Widget

    def __init__(self, widget: Widget) -> None:
        self._w = widget

    def __call__(self, objects: List[game_objects.Object]) -> None:
        for obstacle in objects:
            if isinstance(obstacle.fill(), game_fill.Hex):
                if obstacle:
                    self._w.color = get_color_from_hex(obstacle.fill().value())

                    if isinstance(obstacle, game_objects.Circle):
                        with self._w.canvas:
                            Color(rgba=self._w.color)
                        pos_x = obstacle.center()[0] - obstacle.radius()
                        pos_y = obstacle.center()[1] - obstacle.radius()
                        io_obstacle = io_objects.IO_Circle(
                            diametre=2 * obstacle.radius(),
                            position=[pos_x, pos_y],
                            couleur=obstacle.fill().value(),
                            scale=3,
                        )
                        self._w.canvas.add(io_obstacle)

                    # elif isinstance(obstacle, Circle):
                    #     io_obstacle = self._w.dict_circles.get(obstacle.formID())

                    elif isinstance(obstacle, game_objects.Polygon):
                        if type(obstacle).__name__ == "Kart":
                            self._w.kart_ID = obstacle.formID()
                            with self._w.canvas:
                                Color(rgba=(1, 1, 1, 1))
                                io_obstacle = io_objects.IO_FilledQuadrilateral(
                                    height=16,
                                    width=50,
                                    center=obstacle.center(),
                                    source="client/Images/kartInGame.jpg",
                                    angle=obstacle.angle(),
                                    scale=3,
                                )

                        else:
                            with self._w.canvas:
                                Color(rgba=self._w.color)
                            io_obstacle = io_objects.IO_Polygon(
                                summits=obstacle.vertices(),
                                couleur=obstacle.fill().value(),
                                scale=3,
                            )
                            self._w.canvas.add(io_obstacle)

                    # elif isinstance(obstacle, Polygon):
                    #     io_obstacle = self._w.dict_polygons.get(obstacle.formID())
                    # return io_obstacle

            elif isinstance(obstacle.fill(), game_fill.Pattern):
                if len(obstacle) == 4:
                    if type(obstacle).__name__ == "Gate":
                        with self._w.canvas:
                            io_obstacle = io_objects.IO_Gates(
                                summitsBeforeRotation=obstacle.verticesBeforeRotation(),
                                angle=obstacle.angle(),
                                scale=3,
                            )
                    elif type(obstacle).__name__ == "FinishLine":
                        with self._w.canvas:
                            io_obstacle = io_objects.IO_FinishLine(
                                summitsBeforeRotation=obstacle.verticesBeforeRotation(),
                                angle=obstacle.angle(),
                                scale=3,
                            )
                    else:
                        warning("TO BE IMPLEMENTED")
                        source = obstacle.sourceImage
                        with self._w.canvas:
                            io_obstacle = io_objects.IO_FilledQuadrilateral(
                                summitsBeforeRotation=obstacle.verticesBeforeRotation(),
                                source=source,
                                angle=obstacle.angle(),
                                scale=3,
                            )
                else:
                    raise "Only quadrilaterals can be filled with a pattern"

            else:
                raise "Unsupported color type"