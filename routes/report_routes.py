from fastapi import APIRouter, HTTPException, exception_handlers
from pydantic import BaseModel
from database.db_connection import SetConnection
from database.book_db import BookDB
from database.member_db import MemberDB


router = APIRouter(prefix="/reports")

@router.get("/summary")
def get_summary_router():
    conn = SetConnection.get_connection()

    return {
  "total_books": BookDB.count_total_books(conn),
  "available_books": BookDB.count_available_books(conn),
  "currently_borrowed": BookDB.count_borrowed_books(conn),
  "active_members": MemberDB.count_active_members(conn)
}

@router.get("/books-by-genre")
def get_books_by_genre_router():
    conn = SetConnection.get_connection()
    
    return BookDB.count_by_genre(conn)

@router.get("/top-member")
def get_top_member_router():
    conn = SetConnection.get_connection()
    
    return MemberDB.get_top_member(conn)