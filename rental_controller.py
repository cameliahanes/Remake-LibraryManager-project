from domain.entities import Rental
from controller.undo_controller import FunctionCall, Operation
from datetime import date, timedelta


class BookAuthorRentals(object):
    def __init__(self, author, rental_count):
        self.__author = author
        self.__rental_count = rental_count

    @property
    def book_author(self):
        return self.__author

    @property
    def rental_count(self):
        return self.__rental_count

    def __lt__(self, bookRental):
        """
        Functon to replace the < operator;
        helps for sorting
        """
        return self.rental_count < bookRental.rental_count


class ClientRentalCount(object):
    def __init__(self, client_id, days_rented):
        self.__entity_id = client_id
        self.__days_rented =days_rented

    @property
    def entity_id(self):
        return self.__entity_id

    @property
    def days_rented(self):
        return self.__days_rented

    def __lt__(self, clientRental):
        """
        :return: True/false
        :overrides the < operator, useful for sorting
        """
        return self.days_rented < clientRental.days_rented


class BookCountRented(object):
    def __init__(self, entity_id, count_rented):
        self.__entity_id = entity_id
        self.__count_rented = count_rented

    @property
    def eneity_id(self):
        return self.__entity_id

    @property
    def count_rented(self):
        return self.__count_rented

    def __lt__(self, other):
        return self.count_rented < other.count_rented


class RentalLate(object):
    def __init__(self, entity_id, late):
        self.__entity_id = entity_id
        self.__late = late

    @property
    def entity_id(self):
        return self.__entity_id

    @property
    def late(self):
        return self.__late

    def __lt__(self, other):
        return self.late < other.late


class RentalController(object):
    def __init__(self, rentalRepository, clientController, bookController, undoController):
        self.__rentalRepository = rentalRepository
        self.__clientController = clientController
        self.__bookController = bookController
        self.__undoController = undoController

    def addRental(self, rentalID, bookID, clientID, rentedDate, dueDate, returnedDate):
        self.__rentalRepository.save(Rental(rentalID, bookID, clientID, rentedDate, dueDate, returnedDate))
        redo = FunctionCall(self.addRental, rentalID, bookID, clientID, rentedDate, dueDate, returnedDate)
        undo = FunctionCall(self.removeRental, rentalID)
        operation = Operation(redo, undo)
        self.__undoController.recordOperation(operation)

    def removeRental(self, rentalID):
        bookID = self.findRentalByID(rentalID)[0].book_id
        clientID = self.findRentalByID(rentalID)[0].client_id
        rentedDate = self.findRentalByID(rentalID)[0].rented_date
        dueDate = self.findRentalByID(rentalID)[0].due_date
        returnedDate = self.findRentalByID(rentalID)[0].returned_date
        self.__rentalRepository.remove(rentalID)
        redo = FunctionCall(self.removeRental, rentalID)
        undo = FunctionCall(self.addRental, rentalID, bookID, clientID, rentedDate, dueDate, returnedDate)
        operation = Operation(redo, undo)
        self.__undoController.recordOperation(operation)

    def findRentalByID(self, rentalID):
        for i in self.get_all_rentals():
            if int(i.entity_id) == rentalID:
                return [i]
        return []

    def findRentalByBookID(self, bookID):
        for i in self.get_all_rentals():
            if int(i.book_id) == bookID:
                return [i]
        return []

    def findRentalByClientID(self, clientID):
        for i in self.get_all_rentals():
            if int(i.client_id) == clientID:
                return [i]
        return []

    def get_all_rentals(self):
        return self.__rentalRepository.getAll()

    def get_all_rental_ID(self):
        return self.__rentalRepository.getAllID()

    def updateRental(self, bookID, clientID):
        """
        Thsi function updates the rental, meaning that we return the book
        :param bookID: the id of the book tot be returned
        :param clientID: the id of the client ot return the book
        :raises Exception if the rental was impossible to find
        """
        r = self.findRentalByBookID(bookID)
        if int(r[0].client_id) != clientID:
            raise Exception("Inexistent rental!")
        else:
            rentalID = r[0].entity_id
            rentedDate = r[0].rented_date
            dueDate = r[0].due_date
            firstRetDate = r[0].returned_date
            returnedDate = date.today()
            rental = Rental(rentalID, bookID, clientID, rentedDate, dueDate, returnedDate)
            self.__rentalRepository.update(Rental(rentalID, bookID, clientID, rentedDate, dueDate, returnedDate))
            redo = FunctionCall(self.updateRental, rentalID, bookID, clientID, rentedDate, dueDate, returnedDate)
            undo = FunctionCall(self.updateRental, rentalID, bookID, clientID, rentedDate, dueDate, firstRetDate)
            operation = Operation(redo, undo)
            self.__undoController.recordOperation(operation)

    def filter(self, bookID, clientID, author, late):
        l = []
        """
        l = the list returned
        :returns the list of rentals filtered by book id, client id or if the books are not rented
        """
        for r in self.get_all_rentals():
            if bookID != None and int(r.book_id) != bookID:
                continue
            if clientID != None and int(r.client_id) != clientID:
                continue
            if late != None and r.rented_date != None and int((date.today() - r.rented_date).days()) <= 0:
                continue
            l.append(r)
        return l

    def mostRentedAuthors(self):
        """
        :return: the list of authors and the times their books were rented
        """
        authors = {}
        for book in self.__bookController.get_all_books():
            if book.book_author not in authors.keys():
                authors[book.book_author] = 0
            rentals = self.filter(int(book.entity_id), None, None, None)
            authors[book.book_author] += len(rentals)
            """
            data transfer objects
            """
        dtl = []
        for author in authors.keys():
            dtl.append(BookAuthorRentals(author, authors[author]))
        return dtl.sort(reverse=True)

    def mostActiveClients(self):
        clients = {}
        for client in self.__clientController.get_all_clients():
            if client.entity_id not in clients.keys():
                clients[client.entity_id] = 0
                rentals = self.filter(None, int(client.entity_id), None, None)
                """
                now we have the list of all clients for a certain client
                """
            for r in rentals:
                if r.returned_date == None:
                    clients[client.entity_id] += int((date.today() - r.rented_date).days())
                else:
                    clients[client.entity_id] += int((r.returned_date - r.rented_date).days())
        dtl = []
        for client in clients.keys():
            dtl.append(ClientRentalCount(int(client.entity_id), int(clients[client.entity_id])))
        return dtl.sort(reverse=True)

    def mostRentedBooksDays(self):
        books = {}
        for bk in self.__bookController.get_all_books():
            if bk.entity_id not in books.keys():
                books[bk.entity_id] = 0
            rentals = self.filter(int(bk.entity_id), None, None, None)
            for r in rentals:
                if r.returned_date == None:
                    books[bk.entity_id] += int((date.today() - r.rented_date).days())
                else:
                    books[bk.entity_id] += int((r.returned_date - r.rented_date).days())
        dtl = []
        for book in books.keys():
            dtl.append(BookCountRented(int(book.entity_id), int(books[book.entity_id])))
        return dtl.sort(reverse=True)

    def mostRentedBooksTimes(self):
        books = {}
        for bk in self.__bookController.get_all_books():
            if bk.entity_id not in books.keys():
                books[bk.entity_id] = 0
                rentals = self.filter(int(bk.entity_id), None, None, None)
                books[bk.entity_id] += int(rentals)
        dtl = []
        for book in books.keys():
            dtl.append(BookCountRented(int(book.entity_id), int(books[book.entity_id])))
        return dtl.sort(reverse=True)

    def lateRentals(self):
        rents = {}
        for r in self.__rentalRepository.getAll():
            if r.returned_date == None and int((date.today() - r.rented_date).days()) - 14 > 0:
                rents[r.entity_id] = int((date.today() - r.rented_date).days()) - 14
        dtt = []
        for r in rents:
            dtt.append(RentalLate(int(r.entity_id), int(rents[r.entity_id])))
        return dtt.sort(reverse=True)
