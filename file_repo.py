import collections

from Students.src.repository.file_repository import InexistentIDException, FileRepositoryException


class DuplicatedIDException(FileRepositoryException):
    pass


class FileRepositoryException(Exception):
    pass


class FileRepository(object):

    def __init__(self, validator, filename, entityClass):
        self.__validator = validator
        self.__filename = filename
        self.__entityClass = entityClass
        self.__entities = {}
        self.load_from_file()

    def load_from_file(self):
        try:
            with open(self.__filename) as f:
                for line in f:
                    entity = self.__entityClass.create_entity_csv(line)
                    self.__entities[entity.entity_id] = entity
        except IOError:raise FileRepositoryException("File {0} does not exist!".format(self.__filename))

    def save(self, entity):
        self.__validator.validate(entity)
        if int(entity.entity_id) in self.__entities:
            raise DuplicatedIDException("Duplicated ID!")
        self.__entities[int(entity.entity_id)] = entity
        try:
            with open(self.__filename, "w") as f:
                for e in self.__entities:
                    lst = [e, self.__entities[e]]
                    f.write(self.__entityClass.format_csv(lst))
        except IOError:
            raise FileRepositoryException("File {0} is missong!".format(self.__filename))

    def remove(self, entity_id):
        if not int(entity_id) in self.__entities:
            raise InexistentIDException("Inexistent ID!")
        self.__entities.pop(int(entity_id))
        try:
            with open(self.__filename, "w") as f:
                for entity in self.__entities:
                    lst = [entity, self.__entities[entity]]
                    f.write(self.__entityClass.format_csv(lst))
        except IOError:
            raise FileRepositoryException("File {0} doesn't exist!".format(self.__filename))

    def update(self, entity):
        self.__validator.validate(entity)
        if not int(entity.entity_id) in self.__entities:
            raise InexistentIDException("Inexistent ID!")
        self.__entities[int(entity.entity_id)] = entity
        try:
            with open(self.__filename, "w") as f:
                for entity in self.__entities:
                    lst = [entity, self.__entities[entity]]
                    f.write(self.__entityClass.format_csv(lst))
        except IOError:
            raise FileRepositoryException("File {0} doesn't exist!".format(self.__filename))

    def getAll(self):
        dict = collections.OrderedDict(sorted(self.__entities.items()))
        return list(dict.values())

    def getAllID(self):
        dict = collections.OrderedDict(sorted(self.__entities.items()))
        return list(dict.keys())