from myfastapi.repositories.book_repository import BookRepository

class BookUseCase:
    def __init__(self):
        self.repo = BookRepository()

    def list_books(self, limit=10, offset=0):
        return self.repo.get_all(limit, offset)
