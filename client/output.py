from logging import warning
from typing import Any, Dict, List

from kivy.utils import get_color_from_hex
from kivy.graphics import Color
from kivy.uix.widget import Widget

from game import objects as game_objects
from game.objects import fill as game_fill
from client import io_objects
import lib


class OutputFactory:
    _w: Widget
    _createdObject: Dict[int, Any]
    _maxWidth: float
    _maxHeight: float
    _center: List[float]
    _translate: lib.Vector
    _scale: float
    _initialized: bool

    _gates: List[game_objects.Gate]

    def __init__(
        self,
        widget: Widget,
        max_width: float = None,
        max_height: float = None,
        translate: lib.Vector = lib.Vector(),
        scale: float = 0,
    ) -> None:
        if max_width and max_height:
            self._scale = None
            self._translate = None
            self._maxWidth = max_width
            self._maxHeight = max_height
        elif scale:
            self._translate = translate
            self._scale = scale
        else:
            raise "Either the dimensions or the scale must be given"
        self._w = widget
        self._createdObject = {}
        self._initialized = False

        self._gates = []
    def __call__(self, objects: List[game_objects.Object]) -> None:
        if self._initialized:
            self._w.updateGatesCount(self._gates)

        elif not self._scale:
            # calculer la taille du canvas
            lefts = []
            rights = []
            bottoms = []
            tops = []
            for obj in objects:
                if isinstance(obj, game_objects.Circle):
                    lefts.append(obj.center().x() - obj.radius())
                    rights.append(obj.center().x() + obj.radius())
                    bottoms.append(obj.center().y() - obj.radius())
                    tops.append(obj.center().y() + obj.radius())
                elif isinstance(obj, game_objects.Polygon):
                    vertices = obj.vertices()
                    abscissas = [p.x() for p in vertices]
                    lefts += abscissas
                    rights += abscissas
                    ordinates = [p.y() for p in vertices]
                    bottoms += ordinates
                    tops += ordinates

            leftest = min(lefts)
            rightest = max(rights)
            bottomest = min(bottoms)
            toppest = max(tops)

            self._translate = lib.Vector(
                (
                    (rightest - leftest + self._maxHeight) / 2,
                    (toppest - bottomest + self._maxHeight) / 2,
                )
            )
            self._scale = max(
                (rightest - leftest) / self._maxWidth,
                (toppest - bottomest) / self._maxHeight,
            )

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
        ioCircle = io_objects.Circle(widget=self._w,LGEObject=lgeCircle,scale=self._scale, translate=self._translate)
        self._w.canvas.add(ioCircle)
        self._createdObject[lgeCircle.formID()] = ioCircle

    def createPolygon(self, lgePolygon: game_objects.Polygon) -> None:
        """Dessine le polygon sur le canvas du widget et l'ajout au registre"""
        ioPolygon = io_objects.Polygon(widget=self._w,LGEObject=lgePolygon,scale = self._scale, translate=self._translate)
        self._w.canvas.add(ioPolygon)
        self._createdObject[lgePolygon.formID()] = ioPolygon

    def createKart(self, lgeKart: game_objects.Kart) -> None:
        """Dessine le kart sur le canvas du widget et l'ajout au registre"""
        self._w.kart_ID = lgeKart.formID()
        with self._w.canvas:    # This type of objects has to be put into the 'with self.canvas:' instruction
            Color(rgba=(1, 1, 1, 1))
            ioKart = io_objects.FilledQuadrilateral(LGEObject=lgeKart,source='client/Images/KartInGame.jpg',scale=self._scale, translate=self._translate)
        self._createdObject[lgeKart.formID()] = ioKart

    def createFinishLine(self, lgeFinishLine: game_objects.FinishLine) -> None:
        """Dessine la ligne d'arrivée sur le canvas du widget et l'ajout au registre"""
        with self._w.canvas:
            self._gates.append(lgeFinishLine)
            ioFinishLine = io_objects.FilledQuadrilateral(LGEObject=lgeFinishLine,source='client/Images/finish_line.jpg',scale=self._scale, translate=self._translate)
        self._createdObject[lgeFinishLine.formID()] = ioFinishLine

    def createGate(self, lgeGate: game_objects.Gate) -> None:
        """Dessine la porte sur le canvas du widget et l'ajout au registre"""
        with self._w.canvas:
            self._gates.append(lgeGate)
            ioGate = io_objects.FilledQuadrilateral(LGEObject=lgeGate,source='client/Images/gates.png',scale=self._scale, translate=self._translate)
        self._createdObject[lgeGate.formID()] = ioGate
