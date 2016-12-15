import collections


class RepositoryException(Exception):
    pass


class DuplicatedId(RepositoryException):
    pass


class InexistentId(RepositoryException):
    pass


class Repository(object):

    def __init__(self, validator):
        self.__validator = validator
        self.__entities = {}

    def save(self, entity):
        self.__validator.validate(entity)
        if entity.entity_id in self.__entities:
            raise DuplicatedId("Duplicated ID!")
        self.__entities[entity.entity_id] = entity

    def update(self, entity):
        self.__validator.validate(entity)
        if not entity.entity_id in self.__entities:
            raise InexistentId("Inexistent ID!")
        self.__entities[entity.entity_id] = entity

    def remove(self, entity_id):
        if not entity_id in self.__entities:
            raise InexistentId("Inexistent ID!")
        self.__entities.pop(entity_id)

    def getAll(self):
        return list(collections.OrderedDict(sorted(self.__entities.items())).values())

    def getAllID(self):
        return list(collections.OrderedDict(sorted(self.__entities.items())).keys())