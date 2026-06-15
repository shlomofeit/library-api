from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.book_db import BookDB
from database.member_db import MemberDB
from routes.member_routes import get_member_by_id_router
from enum import Enum
from library_logging import logger


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
    logger.debug("the function was called")

    new_book = book.model_dump()
    if new_book["title"] and new_book["author"] and new_book["genre"]:
        result = BookDB().create_book(new_book)

        logger.info("book created seccessfully: %s", new_book)
        return result

    else:
        logger.warning("essential details were missing to add a book.")

        raise HTTPException(422, {"msg": f"missing params: {book["title"] if not book["title"] else ""} {book["author"] if not book["author"] else ""} {book["genre"] if not book["genre"] else ""}"})

@router.get("")
def get_all_books_router():
    logger.debug("the function was called")

    result = BookDB().get_all_books()
    
    return result if result else []


@router.get("/{id}")
def get_book_by_id_router(id: int):
    logger.debug("the function was called")

    result = BookDB().get_book_by_id(id)

    if result:
        return result
    
    else:
        raise HTTPException(404, {"message": "Book not found"})


@router.patch("/{id}", status_code=201)
def update_book_router(id: int, book: BookValidate):
    logger.debug("the function was called")

    get_book_by_id_router(id)
    new_details_book = book.model_dump(exclude_unset=True)
    new_details_book["genre"] = new_details_book["genre"].value
    return BookDB().update_book(id, new_details_book) > 0


@router.patch("/{id}/borrow/{member_id}")
def borrow_book_router(id: int, member_id: int):
    logger.debug("the function was called")

    book = get_book_by_id_router(id)[0]
    member = get_member_by_id_router(member_id)[0]
    
    if not book["is_availble"]:
        raise HTTPException(400, "Book is not available")
    
    if not member["is_active"]:
        raise HTTPException(400, "Member is not active")
    
    if BookDB().count_active_borrows_by_member(member_id)["COUNT"] > 2:
        raise HTTPException(400, "Member has reached maximum borrows")
    
    BookDB().set_available(id, False, member_id)
    MemberDB().increment_borrows(member_id)

    return {"message": f"The book (ID: {id} ) was successfully borrowed to user: {member_id}"}
    
    
@router.patch("/{id}/return/{member_id}")
def return_book_router(id: int, member_id: int):
    logger.debug("the function was called")

    book = get_book_by_id_router(id)[0]
    member = get_member_by_id_router(member_id)[0]
    
    if book["is_availble"]:
        raise HTTPException(400, "Book is not borrowed")
    
    if not member:
        raise HTTPException(404, "Member not found")
    
    if member["id"] != book["borrowed_by_member_id"]:
        raise HTTPException(400, "Book is not borrowed by this member")
    
    BookDB().set_available(id, True, None)

    return {"message": f"The book (ID: {id} ) was successfully returned from user: {member_id}"}