from fastapi import APIRouter, HTTPException, exception_handlers
from pydantic import BaseModel
from database.db_connection import SetConnection
from database.book_db import BookDB
from database.member_db import MemberDB


router = APIRouter(prefix="/reports")

@router.get("/summary")
def get_summary_router():

    return {
  "total_books": BookDB().count_total_books()[0][0],
  "available_books": BookDB().count_available_books()[0][0],
  "currently_borrowed": BookDB().count_borrowed_books()[0][0],
  "active_members": MemberDB().count_active_members()[0][0]
}

@router.get("/books-by-genre")
def get_books_by_genre_router():
    
    return BookDB().count_by_genre()

@router.get("/top-member")
def get_top_member_router():
    
    return MemberDB().get_top_member()