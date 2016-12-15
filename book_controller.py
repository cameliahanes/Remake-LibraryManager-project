from domain.entities import Book
from  undo_controller import FunctionCall, Operation

class BookController(object):
    def __init__(self, bookRepository, undoController):
        self.__bookRepository = bookRepository
        self.__undoController = undoController

    def addBook(self, bookID, name, description, author):
        self.__bookRepository.save(Book(bookID, name, description, author))
        redo = FunctionCall(self.addBook, bookID, name, description, author)
        undo = FunctionCall(self.removeBook, bookID)
        operation = Operation(redo, undo)
        self.__undoController.recordOperation(operation)


    def removeBook(self, bookID):
        name = self.findByID(bookID)[0].name
        description = self.findByID(bookID)[0].book_description
        author = self.findByID(bookID)[0].book_author
        self.__bookRepository.remove(bookID)
        undo = FunctionCall(self.addBook, bookID, name, description, author)
        redo = FunctionCall(self.removeBook, bookID)
        operation = Operation(redo, undo)
        self.__undoController.recordOperation(operation)


    def updateBookTitle(self, bookID, newTitle):
        title = self.findByID(bookID)[0].name
        description = self.findByID(bookID)[0].book_description
        author = self.findByID(bookID)[0].book_author
        self.__bookRepository.update(Book(bookID, newTitle, description, author))
        redo = FunctionCall(self.updateBookTitle, bookID, newTitle, description, author)
        undo = FunctionCall(self.updateBookTitle, bookID, title, description, author)
        operation = Operation(redo, undo)
        self.__undoController.recordOperation(operation)

    def updateBookDescription(self, bookID, newDesc):
        title = self.findByID(bookID)[0].name
        description = self.findByID(bookID)[0].book_description
        author = self.findByID(bookID)[0].book_author
        self.__bookRepository.update(Book(bookID, title, newDesc, author))
        redo = FunctionCall(self.updateBookDescription, bookID, title, newDesc, author)
        undo = FunctionCall(self.updateBookDescription, bookID, title, description, author)
        operation = Operation(redo, undo)
        self.__undoController.recordOperation(operation)

    def updateBookAuthor(self, bookID, newAuthor):
        title = self.findByID(bookID)[0].name
        description = self.findByID(bookID)[0].description
        author = self.findByID(bookID)[0].book_author
        self.__bookRepository.update(Book(bookID, title, description, newAuthor))
        redo = FunctionCall(self.updateBookAuthor, bookID, title, description, newAuthor)
        undo = FunctionCall(self.updateBookAuthor, bookID, title, description, author)
        operation = Operation(redo, undo)
        self.__undoController.recordOperation(operation)

    def findByID(self, bookID):
        for i in self.get_all_books():
            if int(i.entity_id) == bookID:
                return [i]
        return []

    def findByName(self, name):
        l = []
        for i in self.get_all_clients():
            if name.lower() in i.name.lower():
                l.append(i)
        return l

    def findByDescription(self, desc):
        l = []
        for i in self.get_all_books():
            if desc.lower() in i.book_description.lower():
                l.append(i)
        return l

    def findByAuthor(self, author):
        l = []
        for i in self.get_all_books():
            if author.lower() in i.book_author.lower():
                l.append(i)
        return l

    def findBook(self, args):
        if str(args[0].isdigit()):
            return self.findByID(args[0])
        elif len(str(args[1])) > 0:
            return self.findByName(args[1])
        elif len(str(args[2])) > 0:
            return self.findByDescription(args[2])
        else:
            return self.findByAuthor(args[3])

    def get_all_books(self):
        return self.__bookRepository.getAll()

    def get_all_id(self):
        return self.__bookRepository.getAllID()


