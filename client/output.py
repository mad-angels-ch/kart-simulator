from kivy.graphics.transformation import Matrix
from logging import warning
from typing import Any, Dict, List
from kivy.app import App

from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget

from game import objects as game_objects
from game.objects import fill as game_fill
from client import io_objects
import lib


class OutputFactory:
    _w: Widget
    _frameCallback: "function"
    _createdObject: Dict[int, Any]
    _maxWidth: float
    _maxHeight: float
    _center: List[float]
    _translate: lib.Vector
    _scale: float
    _initialized: bool

    _karts: List[game_objects.Kart]
    _gates: List[game_objects.Gate]
    _finishLine: game_objects.FinishLine

    def __init__(
        self,
        widget: Widget,
        frame_callback: "function" = lambda outup, objects: (),
        max_width: float = None,
        max_height: float = None,
        translate: lib.Vector = lib.Vector(),
        scale: float = 0,
    ) -> None:
        """Instancie et met à jour les objets à afficher"""
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
        self._frameCallback = frame_callback
        self._createdObject = {}
        self._initialized = False

        self._karts = []
        self._gates = []

        self.a = 0
        self.b = 0
        
    def isInitialized(self) -> bool:
        """Retourne vrai si initialisé."""
        return self._initialized

    def getAllKarts(self) -> List[game_objects.Kart]:
        """NE PAS MODIFIER\n
        Retourne la liste de tous les karts du jeu"""
        return self._karts

    def getAllGates(self) -> List[game_objects.Gate]:
        """NE PAS MODIFIER\n
        Retourne tous les portillons du jeu"""
        return self._gates

    def getFinishLine(self) -> game_objects.FinishLine:
        """Retourne la ligne d'arrivée du jeu"""
        return self._finishLine

    def __call__(self, objects: List[game_objects.Object]) -> None:
        self._frameCallback(self, objects)
        if not self._scale:
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

            self._scale = max(
                (rightest - leftest) / self._maxWidth,
                (toppest - bottomest) / self._maxHeight,
            )
            # (two translations and one scaling are required:
            # _translation1 puts the playground at the bottom left (coordinates (0;0)) on the canvas,
            # then _scale fits it to the canvas size,
            # finally _translation2 places it in the center of the canvas.
            # This is purely visual, it doesn't affect the object's physical properties.).translate("french")

            self._translation1 = lib.Vector((-leftest, -bottomest))
            self._translation2 = (
                lib.Vector(
                    (
                        self._maxWidth - (rightest - leftest) / self._scale,
                        self._maxHeight - (toppest - bottomest) / self._scale,
                    )
                )
                / 2
            )
        # self._w.parent.parent.parent.ids.noActionBar.apply_transform(trans=Matrix().translate(1,1,0),anchor=(0,0))
        # self._w.parent.parent.parent.ids.noActionBar.apply_transform(trans=Matrix().scale(self._scale,self._scale,self._scale),anchor=(0,0))
        # self._w.parent.parent.parent.ids.noActionBar.apply_transform(trans=Matrix().translate(self._translation2[0],self._translation2[1],0),anchor=(0,0))

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
                            source = obstacle.fill().source()
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

                self._initialized = True

            else:
                # mettres les positions à jour
                io_object = self._createdObject[obstacle.formID()]
                if isinstance(obstacle, game_objects.Circle):
                    io_object.updatePosition()
                elif isinstance(obstacle, game_objects.Kart):
                    self._w.canvas.remove(io_object)
                    self.createKart(obstacle)
                elif isinstance(obstacle, game_objects.Polygon):
                    io_object.updatePosition()

    def createCircle(self, lgeCircle: game_objects.Circle) -> None:
        """Dessine le cercle sur le canvas du widget et l'ajout au registre"""
        ioCircle = io_objects.Circle(
            widget=self._w,
            LGEObject=lgeCircle,
            scale=self._scale,
            translate1=self._translation1,
            translate2=self._translation2,
        )
        self._w.canvas.add(ioCircle)
        self._createdObject[lgeCircle.formID()] = ioCircle

    def createPolygon(self, lgePolygon: game_objects.Polygon) -> None:
        """Dessine le polygon sur le canvas du widget et l'ajout au registre"""
        ioPolygon = io_objects.Polygon(
            widget=self._w,
            LGEObject=lgePolygon,
            scale=self._scale,
            translate1=self._translation1,
            translate2=self._translation2,
        )
        self._w.canvas.add(ioPolygon)
        self._createdObject[lgePolygon.formID()] = ioPolygon

    def createKart(self, lgeKart: game_objects.Kart) -> None:
        """Dessine le kart sur le canvas du widget et l'ajout au registre"""
        self._w.kart_ID = lgeKart.formID()
        self._karts.append(lgeKart)
        with self._w.canvas:  # Ce type d'objet doit être placé dans l'instruction 'with self.canvas:'
            Color(rgba=(1, 1, 1, 1))
            ioKart = io_objects.FilledQuadrilateral(
                LGEObject=lgeKart,
                source="client/Images/KartInGame.jpg",
                scale=self._scale,
                translate1=self._translation1,
                translate2=self._translation2,
            )
        self._createdObject[lgeKart.formID()] = ioKart
        # with self._w.canvas:
        # #     Rectangle(pos=ioKart.pos)
        # self.a=0
        if not self.a:
            self.a,self.b = ioKart.pos[0],ioKart.pos[1]
            self.an = lgeKart.angle()
            self._w.parent.parent.parent.ids.noActionBar.apply_transform(trans=Matrix().translate(-self.a+100,-self.b+100,0),anchor=(0,0))
            self._w.parent.parent.parent.ids.noActionBar.apply_transform(trans=Matrix().scale(4,4,1),anchor=(0,0))
            # self._w.parent.parent.parent.ids.noActionBar.apply_transform(trans=Matrix().rotate(self.an,ioKart.center[0],ioKart.center[1],0),anchor=(0,0))
            
        self._w.parent.parent.parent.ids.noActionBar.apply_transform(trans=Matrix().translate((-ioKart.pos[0]+self.a)*4,(-ioKart.pos[1]+self.b)*4,0),anchor=(0,0))
        # self._w.parent.parent.parent.ids.noActionBar.apply_transform(trans=Matrix().rotate(lgeKart.angle()-self.an,ioKart.center[0],ioKart.center[1],0),anchor=(0,0))
        self.a,self.b = ioKart.pos[0],ioKart.pos[1]
        self.an = lgeKart.angle()
        
        # self._w.parent.parent.parent.ids.noActionBar.apply_transform(trans=Matrix().translate(self.a[0],self.a[1],0),anchor=(0,0))
        # self._w.parent.parent.parent.ids.noActionBar.apply_transform(trans=Matrix().translate(-ioKart.pos[0],-ioKart.pos[1],0),anchor=(0,0))
        
        # self._w.parent.parent.parent.ids.noActionBar.apply_transform(trans=Matrix().translate(-1,-1,0),anchor=(0,0))
        
        
        
    def createFinishLine(self, lgeFinishLine: game_objects.FinishLine) -> None:
        """Dessine la ligne d'arrivée sur le canvas du widget et l'ajout au registre"""
        with self._w.canvas:
            self._gates.append(lgeFinishLine)
            self._finishLine = lgeFinishLine
            ioFinishLine = io_objects.FilledQuadrilateral(
                LGEObject=lgeFinishLine,
                source="client/Images/finish_line.jpg",
                scale=self._scale,
                translate1=self._translation1,
                translate2=self._translation2,
            )
        self._createdObject[lgeFinishLine.formID()] = ioFinishLine

    def createGate(self, lgeGate: game_objects.Gate) -> None:
        """Dessine le portillon sur le canvas du widget et l'ajout au registre"""
        with self._w.canvas:
            self._gates.append(lgeGate)
            ioGate = io_objects.FilledQuadrilateral(
                LGEObject=lgeGate,
                source="client/Images/gate1.png",
                scale=self._scale,
                translate1=self._translation1,
                translate2=self._translation2,
            )
        self._createdObject[lgeGate.formID()] = ioGate
