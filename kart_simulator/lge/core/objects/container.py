from typing import List
from core.objects.object import Object

from queue import Queue


class Container:
    _objects = list()

    _modifySafe = True
    _modifyQueue = Queue()

    def get_objects(self) -> list:
        return self._objects

    def add_object(self, object: Object, zIndex: int = None) -> None:
        if self._modifySafe:
            if not zIndex:
                self._objects.append(object)
        # else:
        #     self._modifyQueue.put(object, False)

    def __iter__(self):
        return self._objects.__iter__()
