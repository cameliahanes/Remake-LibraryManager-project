class BookException(Exception):
    pass




class BookValidator(object):
    @staticmethod
    def validate(book):
        err = ""
        if len(str(book.entity_id)) == 0:
            err += "Book must have an ID."
        if len(str(book.name)) == 0:
            err += "Book must have a title."
        if len(str(book.book_description)) == 0:
            err += "Book must have a description."
        if len(str(book.book_author)) == 0:
            err += "Book must have an author."
        if not type(book.entity_id) is int:
            err += "ID should be an integer."
        if len(err) > 0:
            raise BookException(err)


class ClientException(Exception):
    pass


class ClientValidator(object):
    @staticmethod
    def validate(client):
        err = ""
        if len(str(client.entity_id)) == 0:
            err += "Client must have an ID."
        if len(str(client.name)) == 0:
            err += "Client must have a name."
        if not type(client.entity_id) is int:
            err += "Client ID must be an integer."
        if len(err) > 0:
            raise ClientException(err)


class RentalException(Exception):
    pass


class RentalValidator(object):
    @staticmethod
    def validate(ren):
        err = ""
        if len(str(ren.entity_id)) == 0:
            err += "Rental must have an ID."
        if len(str(ren.client_id)) == 0:
            err += "Rental must have a client ID."
        if len(str(ren.book_id)) == 0:
            err += "Rental must have a book ID."
        if len(str(ren.rented_date)) == 0:
            err += "Rental should have a rented date."
        if len(str(ren.due_date)) == 0:
            err += "Rental should have a due date."
        if not type(ren.entity_id) is int:
            err += "Rental ID should be an integer."
        if not type(ren.book_id) is int:
            err += "Book ID should be an integer."
        if not type(ren.client_id) is int:
            err += "Client ID should be an integer."
        if len(err) > 0:
            raise RentalException(err)