from fastapi import APIRouter

router = APIRouter(prefix="/reports")

@router.get("/summary")
def get_summary_router():
    pass

@router.get("/books-by-genre")
def get_books_by_genre_router():
    pass

@router.get("/top-member")
def get_top_member_router():
    pass