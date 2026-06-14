from fastapi import APIRouter

router = APIRouter(prefix="/books")

@router.post("")
def create_book_router():
    pass

@router.get("")
def get_all_books_router():
    pass

@router.get("/id")
def get_book_by_id_router():
    pass

@router.patch("/id")
def update_book_router():
    pass

@router.patch("/{id}/borrow/{member_id}")
def borrow_book_router():
    pass

@router.patch("/{id}/return/{member_id}")
def return_book_router():
    pass