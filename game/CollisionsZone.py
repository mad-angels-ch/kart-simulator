from logging import info
from typing import List, Tuple
import os
import time
import math

from lib import Point, Vector
import lib

from . import objects


class CollisionsZone:
    timePrecision = 1e-3

    _timeInterval: float
    _objects: List[objects.Object]
    _dimension: lib.AlignedRectangle

    def __init__(self, timeInterval: float) -> None:
        super().__init__()
        self._timeInterval = timeInterval
        self._objects = list()

    def collides(self, objectToCheck: objects.Object) -> bool:
        """Retourne vrai si l'objet donné en paramètre se trouve dans la zone."""

    def __iadd__(self, objectToAdd: objects.Object) -> None:
        """Ajoute un objet à la zone et redimensionne celle-ci si nécessaire."""
        self._objects.append(objectToAdd)
        # objectCollisionZone: lib.AlignedRectangle = objectToAdd.potentialCollisionZone()

        return self

    def _solveFirst(self, timeInterval: float) -> float:
        # recherche du moment de la collision
        def getCollidedObjects(objects: List[objects.Object]):
            print(halfWorkingInterval)
            for first in range(len(objects) - 1):
                for second in range(first + 1, len(objects)):
                    if objects[first].collides(objects[second], halfWorkingInterval):
                        return (objects[first], objects[second])
            return None

        checkedInterval = 0
        halfWorkingInterval = timeInterval
        lastCollidedObjects = None
        while halfWorkingInterval > self.timePrecision:
            collidedObjects = getCollidedObjects(self._objects)

            if collidedObjects:
                print(collidedObjects[0].collides(collidedObjects[1], 0))
                lastCollidedObjects = collidedObjects
            else:
                for obj in self._objects:
                    obj.updateReferences(halfWorkingInterval)
                if not lastCollidedObjects:
                    # il n'y a aucune collision dans l'intervalle donnée à la fonction
                    return halfWorkingInterval
                checkedInterval += halfWorkingInterval
            halfWorkingInterval /= 2

        # gestion de la collision
        # print("Collision entre", lastCollidedObjects[0].formID(), "et", lastCollidedObjects[1].formID())
        point, tangent = lastCollidedObjects[0].collisionPointAndTangent(
            lastCollidedObjects[1]
        )
        angle = tangent.direction()

        masses = [obj.mass() for obj in lastCollidedObjects]
        objSpeeds = [obj.vectorialMotionSpeed() for obj in lastCollidedObjects]
        pointSpeeds = [obj.speedAtPoint(point) for obj in lastCollidedObjects]
        speedsBefore = objSpeeds.copy()
        speedsBefore.extend(pointSpeeds)
        for speed in speedsBefore:
            speed.rotate(-angle)
        speedsAfter = [Vector(speed) for speed in objSpeeds]

        other = len(masses) - 1
        for current in range(len(masses)):
            m1 = masses[current]
            m2 = masses[other]
            v1 = objSpeeds[current][1]
            v2 = pointSpeeds[other][1]

            if m1:
                if m2:
                    speedsAfter[current][1] = 2 * (m1 * v1 + m2 * v2) / (m1 + m2) - v1
                else:
                    speedsAfter[current][1] = 2 * v2 - v1
            else:
                if m2:
                    speedsAfter[current][1] = v1
                else:
                    raise "Collision between two fixed objects"

            other = current

        for current in range(len(masses)):
            speedsAfter[current].rotate(angle)
            # speedsAfter[current] *= (1 - lastCollidedObjects[current].friction()) * (
            #     1 - lastCollidedObjects[other].friction()
            # )
            lastCollidedObjects[current].onCollision(lastCollidedObjects[other])
            lastCollidedObjects[current].set_vectorialMotionSpeed(speedsAfter[current])

            other = current

        print("collision", speedsAfter[0].x())
        return checkedInterval

    def resolve(self) -> None:
        while self._timeInterval > 0:
            self._timeInterval -= self._solveFirst(self._timeInterval)
