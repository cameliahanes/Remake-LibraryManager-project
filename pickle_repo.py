import pickle

import collections


class InexistentIDException(Exception):
    pass


class DuplicatedIDException(Exception):
    pass


class PickleRepository():
    def __init__(self, validator, file, restoreState = True):
        self._now = 0
        self._entities = {}
        # this one will receive the list of entities
        self._store = restoreState
        self.__validator = validator
        self.__filename = file

        if restoreState:
            self.restoreHistory()
        else:
            self.createFreshRepo()

    def load_from_file(self):
        try:
            with open(self.__filename, "rb") as f:
                self = pickle.load(f)
        except IOError:
            raise Exception("Couldn't find file..")

    def getNowIndex(self):
        return self._now

    def getAll(self):
        dct =  collections.OrderedDict(sorted(self._entities.items()))
        return dct.values()

    def save(self, entity):
        #newState = self.getStateCopy()
        self.__validator.validate(entity)
        if (entity.entity_id) in self._entities:
            raise DuplicatedIDException("Duplicated ID!")
        self._entities[(entity.entity_id)] = entity
        try:
            with open(self.__filename, "wb") as f:
                #for e in self._entities:
                 #   lst = [e, self._entities[e]]
                  #  pickle.dump(lst, f)
                self._now += 1
                pickle.dump(self, f)
        except IOError:
            raise Exception("Error at saving entity...")

    def remove(self, entity_id):
        if not entity_id in self._entities:
            raise InexistentIDException("Inexistent ID!")
        self._entities.pop((entity_id))
        try:
            with open('repository\history.bin', "wb") as f:
                #for e in self._entities:
                 #   lst = [e, self._entities[e]]
                  #  pickle.dump(lst, f)
                self._now += 1
                pickle.dump(self, f)
        except IOError:
            raise Exception("Error at storing data...")

    def update(self, entity):
        self.__validator.validate(entity)
        if not entity.entity_id in self._entities:
            raise InexistentIDException("Inexistent ID!")
        self._entities[(entity.entity_id)] = entity
        try:
            with open(self.__filename, "wb") as f:
                #for e in self._entities:
                 #   lst = [e, self._entities[e]]
                  #  pickle._dump(lst, f)
                self._now += 1
                pickle.dump(self, f)
        except IOError:
            raise Exception("Error at storing data into database...")

    def restoreHistory(self):
        try:
            with open(self.__filename, "rb") as f:
                self.load_from_file()
        except IOError:
            self.createFreshRepo()

    def createFreshRepo(self):
        self._entities = {}
        self._now = 0