from fastapi import APIRouter, HTTPException
from myfastapi.usecases.book_usecase import BookUseCase
from myfastapi.schemas.book_schema import BookSchema
from typing import List

router = APIRouter(prefix="/books", tags=["Books"])
usecase = BookUseCase()

@router.get("/", response_model=List[BookSchema])
def get_books(limit: int = 10, offset: int = 0):
    return usecase.list_books(limit, offset)

@router.get("/{book_id}", response_model=BookSchema)
def get_book_by_id(book_id: int):
    book = usecase.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/category/{category_name}", response_model=List[BookSchema])
def get_books_by_category(category_name: str, limit: int = 10, offset: int = 0):
    books = usecase.get_books_by_category(category_name, limit, offset)
    if not books:
        raise HTTPException(status_code=404, detail=f"No books found in category '{category_name}'")
    return books
