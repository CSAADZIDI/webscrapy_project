from myfastapi.database import get_connection
from myfastapi.models.book_model import Book

class BookRepository:
    def get_all(self, limit=10, offset=0):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT TOP (?) * FROM Books", (limit,))
            rows = cursor.fetchall()
            return [Book(*row) for row in rows]
