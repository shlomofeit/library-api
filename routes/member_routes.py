from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.member_db import MemberDB
from mysql import connector
from library_logging import logger


class MemberValidate(BaseModel):
    name: str | None = None
    email: str | None = None
    

router = APIRouter(prefix="/members")

@router.post("", status_code=201)
def create_member_router(member: MemberValidate):
    logger.debug("the function was called")

    new_member = member.model_dump(exclude_unset=True)

    if new_member["name"] and new_member["email"]:
        
        try:
            MemberDB().create_member(new_member)
            return {"message": "user created successfully"}
        except connector.errors.IntegrityError:
            raise HTTPException(409, {"message": "Email address already exists in the system. Duplicate registration is not possible."})

    else:
        raise HTTPException(422, {"msg": f"missing params: {member["name"] if not member["name"] else ""} {member["email"] if not member["email"] else ""}"})

@router.get("")
def get_all_members_router():
    logger.debug("the function was called")

    result = MemberDB().get_all_members()

    return result if result else []


@router.get("/{id}")
def get_member_by_id_router(id: int):
    logger.debug("the function was called")

    result = MemberDB().get_member_by_id(id)

    if result:
        return result
    
    raise HTTPException(404, {"message": "Member not found"})


@router.patch("/{id}", status_code=201)
def update_member_router(id: int, member: MemberValidate):
    logger.debug("the function was called")

    get_member_by_id_router(id)
    member_detail = member.model_dump(exclude_unset=True)

    MemberDB().get_member_by_id(id)
    
    MemberDB().update_member(id, member_detail)    
    return {"message": "Member updated successfully"}


@router.patch("/{id}/deactivate")
def deactive_member_router(id: int):
    logger.debug("the function was called")

    get_member_by_id_router(id)

    MemberDB().get_member_by_id(id)    
    
    MemberDB().deactivate_member(id)    
    return {"message": "Member updated successfully"}

@router.patch("/{id}/activate")
def active_member_router(id: int):
    logger.debug("the function was called")

    get_member_by_id_router(id)

    MemberDB().get_member_by_id(id)

    MemberDB().activate_member(id)    
    return {"message": "Member updated successfully"}