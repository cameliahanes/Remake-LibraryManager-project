from domain.entities import Client
from undo_controller import FunctionCall, Operation


class ClientController(object):
    def __init__(self, clientRepository, undoController):
        self.__clientRepository = clientRepository
        self.__undoController = undoController

    def addClient(self, clientID, name):
        self.__clientRepository.save(Client(clientID, name))
        redo = FunctionCall(self.addClient, clientID, name)
        undo = FunctionCall(self.removeClient, clientID)
        operation = Operation(redo, undo)
        self.__undoController.recordOperation(operation)


    def removeClient(self, clientID):
        name = self.findByID(clientID)[0].name
        self.__clientRepository.remove(clientID)

        redo = FunctionCall(self.removeClient, clientID)
        undo = FunctionCall(self.addClient, clientID, name)
        operation = Operation(redo, undo)
        self.__undoController.recordOperation(operation)


    def updateClientName(self, clientID, newName):
        name = self.findByID(clientID)[0].name

        self.__clientRepository.update(Client(clientID, newName))
        redo = FunctionCall(self.updateClientName, clientID, newName)
        undo = FunctionCall(self.updateClientName, clientID, name)
        operation = Operation(redo, undo)
        self.__undoController.recordOperation(operation)

    def findByID(self, clientID):
        for i in self.get_all_clients():
            if int(i.entity_id) == clientID:
                return [i]
        return []

    def get_all_clients(self):
        return self.__clientRepository.getAll()

    def get_all_id(self):
        return self.__clientRepository.getAllID()

    def findByName(self, name):
        l = []
        for i in self.get_all_clients():
            if name.lower() in i.name.lower():
                l.append(i)
        return l

    def findClient(self, args):
        if str(args[0].isdigit()):
            return self.findByID(args[0])
        else:
            return self.findByName(args[0])

