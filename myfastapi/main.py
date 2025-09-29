from fastapi import FastAPI
from myfastapi.routers import books_router

app = FastAPI(title="Books API")

app.include_router(books_router.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Books API"}
