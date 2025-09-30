from myfastapi.repositories.book_repository import BookRepository

class BookUseCase:
    def __init__(self):
        self.repo = BookRepository()

    def list_books(self, limit=10, offset=0):
        return self.repo.get_all(limit, offset)
    
    def get_book_by_id(self, book_id: int):
        """Récupérer un livre par son ID"""
        return self.repo.get_book_by_id(book_id)

    def get_books_by_category(self, category: str, limit: int = 10, offset: int = 0):
        """Récupérer tous les livres d'une catégorie spécifique"""
        return self.repo.get_books_by_category(category, limit=limit, offset=offset)
