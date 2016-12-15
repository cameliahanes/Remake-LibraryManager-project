class Book(object):
    def __init__(self, id, title, description, author):
        '''
        Constructor
        '''
        self.__id = id
        self.__title = title
        self.__description = description
        self.__author = author

    @property
    def entity_id(self):
        return self.__id

    @property
    def name(self):
        return self.__title

    @property
    def book_description(self):
        return self.__description

    @property
    def book_author(self):
        return self.__author

class Client(object):
    def __init__(self, id, name):
        self.__id = id
        self.__name = name

    @property
    def entity_id(self):
        return self.__id

    @property
    def name(self):
        return self.__name


class Rental(object):
    def __init__(self, rentalID, bookID, clientID, rentedDate, dueDate, returnedDate):
        self.__rentalID = rentalID
        self.__bookID = bookID
        self.__clientID = clientID
        self.__rentedDate = rentedDate
        self.__dueDate = dueDate
        self.__returnedDate = returnedDate

    @property
    def entity_id(self):
        return  self.__rentalID

    @property
    def book_id(self):
        return self.__bookID

    @property
    def client_id(self):
        return self.__clientID

    @property
    def rented_date(self):
        return self.__rentedDate

    @property
    def due_date(self):
        return self.__dueDate

    @property
    def returned_date(self):
        return self.__returnedDate