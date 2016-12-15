from datetime import date, timedelta


class Console(object):
    def __init__(self, client_controller, book_controller, rental_controller, undo_controller):
        self.__client_controller = client_controller
        self.__book_controller = book_controller
        self.__rental_controller = rental_controller
        self.__undo_controller = undo_controller

    def runApp(self):
        self.menuBased()


    def uiAddClient(self, args):
        self.__client_controller.addClient(int(args[0]), str(args[1]))

    def uiRemoveClient(self, args):
        self.__client_controller.removeClient(int(args[0]))

    def uiUpdateClient(self, args):
        self.__client_controller.updateClientName(int(args[0]), str(args[1]))

    def uiListClients(self, args):
        for i in self.__client_controller.get_all_clients():
            print("Client with ID: {0} and name: {1}".format(i.entity_id, i.name))

    def searchClients(self, args):
        l = self.__client_controller.findClient(args)
        if len(l) == 0:
            print("No client found!")
        else:
            for i in l:
                print("Client with ID: {0} and name: {1}".format(i.entity_id, i.name))

    def uiAddBook(self, args):
        self.__book_controller.addBook(int(args[0]), str(args[1]), str(args[2]), str(args[3]))

    def uiRemoveBook(self, args):
        self.__book_controller.removeBook(int(args[0]))

    def uiUpdateBookTitle(self, args):
        self.__book_controller.updateBookTitle(int(args[0]), str(args[1]))

    def uiUpdateBookDescription(self, args):
        self.__book_controller.updateBookDescription(int(args[0]), str(args[1]))

    def uiUpdateBookAuthor(self, args):
        self.__book_controller.updateBookAuthor(int(args[0]), str(args[1]))

    def uiListBooks(self, args):
        for i in self.__book_controller.get_all_books():
            print("Book with ID: {0}, title: {1}, description: {2} and author: {3}.".format(i.entity_id, i.name, i.book_description, i.book_author))

    def searchBooks(self, args):
        l = self.__book_controller.findBook(args)
        if len(l) == 0:
            print("No book found!")
        else:
            for i in l:
                print("Book with ID: {0}, title: {1}, description: {2} and author: {3}.".format(i.entity_id, i.name, i.book_description, i.book_author))

    def uiAddRental(self, args):
        self.__rental_controller.addRental(int(args[0]), int(args[1]), int(args[2]), date.today(), date.today()+timedelta(days=14), None)

    def uiReturnBook(self, args):
        self.__rental_controller.updateRental(int(args[0]), int(args[1]))

    def uiMostRentedBooksDays(self, args):
        books = self.__rental_controller.mostRentedBooksDays()
        for b in books:
            print("Book with ID: {0} rented {1} days.".format(b.entity_id, b.count_rented))

    def uiMostRentedBooksTimes(self, args):
        books = self.__rental_controller.mostRentedBooksTimes()
        for b in books:
            print("Book with ID: {0} rented {1} times".format(b.entity_id, b.count_rented))

    def uiMostRentedAuthors(self, args):
        authors = self.__rental_controller.mostRentedAuthors()
        for a in authors:
            print("Author {0} has {1} days of rental.".format(a.book_author, a.rental_count))

    def uiMostActiveClients(self, args):
        clients = self.__rental_controller.mostActiveClients()
        for c in clients:
            print("Client with ID: {0} has {1} days of rental.".format(c.client_id, c.days_rented))

    def uiLateRentals(self, args):
        rents = self.__rental_controller.lateRentals()
        if len(rents) == 0:
            print("No late rental, congratulations!")
        else:
            for r in rents:
                print("Rental with ID: {0} has overdue of {1} days.".format(r.entity_id, r.late))

    def uiPrintAllRentals(self, args):
        rents = self.__rental_controller.get_all_rentals()
        for r in rents:
            print("Rental with ID: {0}, book ID: {1}, client ID: {2}, rented date: {3}, due date: {4}, returned date: {5}."\
                  .format(r.entity_id, r.book_id, r.client_id, r.rented_date, r.due_date, r.returned_date))

    def printOptionsAttributes(self, attr):
        args = []
        for i in attr:
            print(i, end="")
            args.append(input())
        return args

    def uiUndo(self, args):
        self.__undo_controller.undo()

    def uiRedo(self, args):
        self.__undo_controller.redo()

    def statisticsMenu(self, args):
        opts = {"1":self.uiMostActiveClients, "2":self.uiMostRentedAuthors, "3":self.uiMostRentedBooksDays, \
                "4":self.uiMostRentedBooksTimes, "5":self.uiLateRentals}
        attrs = {"1":[], "2":[], "3":[], "4":[], "5":[]}
        while True:
            try:
                cmd = input("Enter option: ")
                if cmd not in opts.keys():
                    raise Exception("Unknown statistics command...")
                argss = self.printOptionsAttributes(attrs[cmd])
                opts[cmd](argss)
            except Exception as ex:
                print(ex)

    def menuBased(self):
        options = {"1": self.uiAddClient, "2": self.uiRemoveClient, "3": self.uiUpdateClient, \
                   "4": self.uiListClients, "5": self.searchClients, "0":self.uiUndo, "-1":self.uiRedo, \
                   "6":self.uiAddBook, "7":self.uiRemoveBook, "8":self.uiUpdateBookTitle, "9": self.uiUpdateBookDescription, \
                   "10":self.uiUpdateBookAuthor,  "11":self.uiListBooks, "12":self.searchBooks, "13":self.statisticsMenu, \
                   "14":self.uiAddRental, "15":self.uiReturnBook, "16":self.uiPrintAllRentals
                   }

        atributes = {"1":["Client ID: ", "Client name: "], "2":["Client ID: "], "3":["Client ID: ", "Client name: "], "4":[], "5":["Client ID/name: "],
                     "0":[], "-1":[], "6":["Book ID: ", "Book title: ", "Book description: ", "Book author: "], "7":["Book ID: "], \
                     "8":["Book ID: ", "Book title: "], "9":["Book ID: ","Book description: "], "10":["Book ID: ","Book author: "], "11":[], \
                     "12":["Book ID/ title/ description/ author: "], "13":[], "14":["Rental ID: ",\
                        "Book ID: ", "Client ID: "], "15":["Book ID: ", "Client ID: "], "16":[]
                     }

        #, "Rented date set.":[date.today()], "Due date set.":[date.today()+timedelta(days = 14)], "To be returned.":[None]

        while True:

            try:
                command = input("Enter command: ")
                if command not in options.keys():
                    raise Exception("Unknown command...")
                args = self.printOptionsAttributes(atributes[command])
                if str(command) in ["1", "2", "3", "6", "7", "8", "9", "10"]:
                    self.__undo_controller.newOperation()
                options[command](args)
            except Exception as ex:
                print(ex)
