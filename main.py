from controller.client_controller import ClientController
from controller.book_controller import BookController
from controller.rental_controller import RentalController
from domain.validators import BookValidator, ClientValidator, RentalValidator
from repository.repo import Repository
from ui.console import Console
from undo_controller import UndoController


def runApp():
    book_repository = Repository(BookValidator)
    client_repository = Repository(ClientValidator)
    rental_repository = Repository(RentalValidator)

    undo_controller = UndoController()

    client_controller = ClientController(client_repository, undo_controller)
    book_controller = BookController(book_repository, undo_controller)
    rental_controller = RentalController(rental_repository, client_controller, book_controller, undo_controller)
    console = Console(client_controller, book_controller, rental_controller, undo_controller)
    console.runApp()

if __name__ == '__main__':
    runApp()
