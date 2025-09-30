from myfastapi.infrastructure.database import get_connection
from myfastapi.models.book_model import Book

class BookRepository:
    def get_all(self, limit=10, offset=0):
        """Récupérer tous les livres avec pagination"""
        with get_connection() as conn:
            cursor = conn.cursor()
            query = """
                SELECT *
                FROM Books
                ORDER BY id
                OFFSET ? ROWS
                FETCH NEXT ? ROWS ONLY;
            """
            cursor.execute(query, (offset, limit))
            rows = cursor.fetchall()
            return [Book(*row) for row in rows]

    def get_book_by_id(self, book_id: int):
        """Récupérer un livre par son ID"""
        with get_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM Books WHERE id = ?"
            cursor.execute(query, (book_id,))
            row = cursor.fetchone()
            return Book(*row) if row else None

    def get_books_by_category(self, category: str, limit=10, offset=0):
        """Récupérer les livres par catégorie avec pagination"""
        with get_connection() as conn:
            cursor = conn.cursor()
            query = """
                SELECT *
                FROM Books
                WHERE category = ?
                ORDER BY id
                OFFSET ? ROWS
                FETCH NEXT ? ROWS ONLY;
            """
            cursor.execute(query, (category, offset, limit))
            rows = cursor.fetchall()
            return [Book(*row) for row in rows]
