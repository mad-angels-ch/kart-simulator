from logging import warning

from kivy.utils import get_color_from_hex
from kivy.graphics import Color

from game import objects as game_objects
from game.objects import fill as game_fill
import io_objects


def output(self, objects) -> None:
    for obstacle in objects:
        if isinstance(obstacle.fill(), game_fill.Hex):
            if obstacle:
                self.color = get_color_from_hex(obstacle.fill().value())

                if isinstance(obstacle, game_objects.Circle):
                    with self.canvas:
                        Color(rgba=self.color)
                    pos_x = obstacle.center()[0] - obstacle.radius()
                    pos_y = obstacle.center()[1] - obstacle.radius()
                    io_obstacle = io_objects.IO_Circle(
                        diametre=2 * obstacle.radius(),
                        position=[pos_x, pos_y],
                        couleur=obstacle.fill().value(),
                        scale=3,
                    )
                    self.canvas.add(io_obstacle)

                # elif isinstance(obstacle, Circle):
                #     io_obstacle = self.dict_circles.get(obstacle.formID())

                elif isinstance(obstacle, game_objects.Polygon):
                    if type(obstacle).__name__ == "Kart":
                        self.kart_ID = obstacle.formID()
                        with self.canvas:
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
                        with self.canvas:
                            Color(rgba=self.color)
                        io_obstacle = io_objects.IO_Polygon(
                            summits=obstacle.vertices(),
                            couleur=obstacle.fill().value(),
                            scale=3,
                        )
                        self.canvas.add(io_obstacle)

                # elif isinstance(obstacle, Polygon):
                #     io_obstacle = self.dict_polygons.get(obstacle.formID())
                # return io_obstacle

        elif isinstance(obstacle.fill(), game_fill.Pattern):
            if len(obstacle) == 4:
                if type(obstacle).__name__ == "Gate":
                    with self.canvas:
                        io_obstacle = io_objects.IO_Gates(
                            summitsBeforeRotation=obstacle.verticesBeforeRotation(),
                            angle=obstacle.angle(),
                            scale=3,
                        )
                elif type(obstacle).__name__ == "FinishLine":
                    with self.canvas:
                        io_obstacle = io_objects.IO_FinishLine(
                            summitsBeforeRotation=obstacle.verticesBeforeRotation(),
                            angle=obstacle.angle(),
                            scale=3,
                        )
                else:
                    warning("TO BE IMPLEMENTED")
                    source = obstacle.sourceImage
                    with self.canvas:
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
