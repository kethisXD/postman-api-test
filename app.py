from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Book API for Postman Testing")

class BookCreate(BaseModel):
    title: str
    author: Optional[str] = "Unknown"

class Book(BookCreate):
    id: int

books_db = {}
current_id = 1

@app.post("/books", response_model=Book)
def create_book(book: BookCreate, x_user_id: str = Header(..., alias="X-User-Id")):
    global current_id
    new_book = Book(id=current_id, **book.dict())
    books_db[current_id] = new_book
    current_id += 1
    return new_book

@app.get("/books", response_model=List[Book])
def get_all_books():
    return list(books_db.values())

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    return books_db[book_id]

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookCreate, x_user_id: str = Header(..., alias="X-User-Id")):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    updated_book = Book(id=book_id, **book.dict())
    books_db[book_id] = updated_book
    return updated_book

@app.delete("/books/{book_id}")
def delete_book(book_id: int, x_user_id: str = Header(..., alias="X-User-Id")):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    del books_db[book_id]
    return {"message": "Book deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
