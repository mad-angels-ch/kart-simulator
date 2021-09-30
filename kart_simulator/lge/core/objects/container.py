from configparser import Error
from core.objects.object import Object


class Container:
    _objects = dict()

    _requests = list()

    def get_all(self) -> list:
        return self._objects
        
    def add(self, toAdd: Object) -> None:
        self._requests.append(toAdd)

    def modify(self, toModify: Object) -> None:
        self._requests.append(toModify)

    def remove(self, byFormID: int = None, byObject: Object = None, byName: str = None) -> None:
        if byFormID:
            self._requests.append(byFormID)
        elif byObject:
            self._requests.append(byObject.get_formID())
        elif byName:
            for object in self:
                if object.get_name() == byName:
                    self._requests.append(object.get_formID())
        else:
            raise Error("Container: No object to remove !")

    def handleRequests(self) -> None:
        for request in self._requests:
            if type(request) == str:
                # supprimer l'objet
                self._objects.pop(request)
            else:
                # ajouter/modifier l'objet
                self._objects[request.get_formID()] = request

    def __iter__(self):
        return self._objects.__iter__()
