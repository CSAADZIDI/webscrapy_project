from fastapi import APIRouter
from myfastapi.usecases.book_usecase import BookUseCase
from myfastapi.schemas.book_schema import BookSchema
from typing import List

router = APIRouter(prefix="/books", tags=["Books"])
usecase = BookUseCase()

@router.get("/", response_model=List[BookSchema])
def get_books(limit: int = 10, offset: int = 0):
    return usecase.list_books(limit, offset)
