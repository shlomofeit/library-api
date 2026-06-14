from fastapi import APIRouter

router = APIRouter(prefix="/members")

@router.post("")
def create_member_router():
    pass

@router.get("")
def get_all_members_router():
    pass

@router.get("/id")
def get_member_by_id_router():
    pass

@router.patch("/id")
def update_member_router():
    pass

@router.patch("/{id}/deactivate")
def deactive_member_router():
    pass

@router.patch("/{id}/activate")
def active_member_router():
    pass