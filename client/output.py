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

    def __call__(self, objects: List[game_objects.Object]) -> None:
        if self._initialized:
            self._w.updateGatesCount(self._gates)

        else:
            # calculer la taille du canvas
            pass

        for obstacle in objects:
            if not self._initialized or obstacle.formID() not in self._createdObject:
                if isinstance(obstacle, game_objects.Kart):
                    self.createKart(obstacle)

                elif isinstance(obstacle.fill(), game_fill.Hex):
                    if isinstance(obstacle, game_objects.Circle):
                        self.createCircle(obstacle)
                    elif isinstance(obstacle, game_objects.Polygon):
                        self.createPolygon(obstacle)

                elif isinstance(obstacle.fill(), game_fill.Pattern):
                    if len(obstacle) == 4:
                        if isinstance(obstacle, game_objects.FinishLine):
                            self.createFinishLine(obstacle)
                        elif isinstance(obstacle, game_objects.Gate):
                            self.createGate(obstacle)
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
                            self._createdObject[obstacle.formID()] = io_obstacle
                    else:
                        raise "Only quadrilaterals can be filled with a pattern"

                else:
                    raise "Unsupported color type"

            else:
                # mettres les positions à jour
                io_object = self._createdObject[obstacle.formID()]
                if isinstance(obstacle, game_objects.Circle):
                    io_object.updatePosition(newPos=obstacle.center())
                elif isinstance(obstacle, game_objects.Kart):
                    self._w.canvas.remove(io_object)
                    self.createKart(obstacle)
                elif isinstance(obstacle, game_objects.Polygon):
                    io_object.updatePosition(newPos=obstacle.vertices())
                    if isinstance(obstacle, game_objects.FinishLine):
                        self._w.updateLapsCount(obstacle)

        self._initialized = True

    def createCircle(self, lgeCircle: game_objects.Circle) -> None:
        """Dessine le cercle sur le canvas du widget et l'ajout au registre"""
        ioCircle = io_objects.Circle(widget=self._w,LGEObject=lgeCircle,scale=self._scale)
        self._w.canvas.add(ioCircle)
        self._createdObject[lgeCircle.formID()] = ioCircle

    def createPolygon(self, lgePolygon: game_objects.Polygon) -> None:
        """Dessine le polygon sur le canvas du widget et l'ajout au registre"""
        ioPolygon = io_objects.Polygon(widget=self._w,LGEObject=lgePolygon,scale = self._scale)
        self._w.canvas.add(ioPolygon)
        self._createdObject[lgePolygon.formID()] = ioPolygon

    def createKart(self, lgeKart: game_objects.Kart) -> None:
        """Dessine le kart sur le canvas du widget et l'ajout au registre"""
        self._w.kart_ID = lgeKart.formID()
        with self._w.canvas:    # This type of objects has to be put into the 'with self.canvas:' instruction
            Color(rgba=(1, 1, 1, 1))
            ioKart = io_objects.FilledQuadrilateral(LGEObject=lgeKart,source='client/Images/KartInGame.jpg',scale=self._scale)
        self._createdObject[lgeKart.formID()] = ioKart

    def createFinishLine(self, lgeFinishLine: game_objects.FinishLine) -> None:
        """Dessine la ligne d'arrivée sur le canvas du widget et l'ajout au registre"""
        with self._w.canvas:
            self._gates.append(lgeFinishLine)
            ioFinishLine = io_objects.FilledQuadrilateral(LGEObject=lgeFinishLine,source='client/Images/finish_line.jpg',scale=self._scale)
        self._createdObject[lgeFinishLine.formID()] = ioFinishLine

    def createGate(self, lgeGate: game_objects.Gate) -> None:
        """Dessine la porte sur le canvas du widget et l'ajout au registre"""
        with self._w.canvas:
            self._gates.append(lgeGate)
            ioGate = io_objects.FilledQuadrilateral(LGEObject=lgeGate,source='client/Images/gates.png',scale=self._scale)
        self._createdObject[lgeGate.formID()] = ioGate
