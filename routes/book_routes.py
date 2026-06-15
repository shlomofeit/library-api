from fastapi import APIRouter, HTTPException, exception_handlers
from pydantic import BaseModel
from database.db_connection import SetConnection
from database.book_db import BookDB
from database.member_db import MemberDB
from enum import Enum


class Genre(str, Enum):
    Fiction = "Fiction"
    Non_Fiction = "Non-Fiction"
    Science = "Science"
    History = "History"
    Other = "Other"

class BookValidate(BaseModel):
    title: str | None = None
    author: str | None = None
    genre: Genre | None = None



router = APIRouter(prefix="/books")

@router.post("", status_code=201)
def create_book_router(book: BookValidate):
    new_book = book.model_dump()
    if book["title"] and book["author"] and book["genre"]:
        conn = BookDB(SetConnection.get_connection())
        conn.create_book(new_book)

    else:
        raise HTTPException(422, {"msg": f"missing params: {book["title"] if not book["title"] else ""} {book["author"] if not book["author"] else ""} {book["genre"] if not book["genre"] else ""}"})

@router.get("")
def get_all_books_router():
    conn = BookDB(SetConnection.get_connection())
    result = conn.get_all_books()

    return result if result else []


@router.get("/{id}")
def get_book_by_id_router(id: int):
    conn = BookDB(SetConnection.get_connection())
    result = conn.get_book_by_id(id)

    if result:
        return result
    
    else:
        raise HTTPException(404, {"message": "Book not found"})


@router.patch("/{id}", status_code=201)
def update_book_router(id: int, book: BookValidate):
    new_details_book = book.model_dump(exclude_unset=True)
    conn = BookDB(SetConnection.get_connection())
    conn.update_book(id, new_details_book)


@router.patch("/{id}/borrow/{member_id}")
def borrow_book_router(id: int, member_id: int):
    conn = SetConnection.get_connection()
    book = BookDB.get_book_by_id(conn, id)
    member = MemberDB.get_member_by_id(conn, member_id)

    if not book:
        raise HTTPException(404, {"message": "Book not found"})
    
    if not book["is_availble"]:
        raise HTTPException(400, "Book is not available")
    
    if not member:
        raise HTTPException(404, "Member not found")
    
    if not member["is_active"]:
        raise HTTPException(400, "Member is not active")
    
    if member["total_borrows"] > 2:
        raise HTTPException(400, "Member has reached maximum borrows")
    
    BookDB.set_available(conn, id, False, member_id)
    MemberDB.increment_borrows(conn, member_id)

    return {"message": f"The book (ID: {id} ) was successfully borrowed to user: {member_id}"}
    
    
@router.patch("/{id}/return/{member_id}")
def return_book_router(id: int, member_id: int):
    conn = SetConnection.get_connection()
    book = BookDB.get_book_by_id(conn, id)
    member = MemberDB.get_member_by_id(conn, member_id)
    if not book:
        raise HTTPException(404, "Book not found")
    
    if book["is_availble"]:
        raise HTTPException(400, "Book is not borrowed")
    
    if not member:
        raise HTTPException(404, "Member not found")
    
    if member["id"] == book["borrowed_by_member_id"]:
        raise HTTPException(400, "Book is not borrowed by this member")
    
    BookDB.set_available(conn, id, True, None)

    return {"message": f"The book (ID: {id} ) was successfully returned from user: {member_id}"}