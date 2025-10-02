from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model, schemas
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from sqlalchemy import update, desc
from datetime import time

from repository.allocate import broker_allocate_single, broker_search_allocate, researcher_accept_allocate, researcher_reject_allocate, researcher_search_allocate
from repository.log import get_logs
from repository.projects import *
from repository.proposal import researcher_get_proposals_like, researcher_update_proposal_and__not_add_project, researcher_update_proposal_and_add_project
from repository.reports import *
from model.schemas import *
from repository.user import admin_get_users_like
import util
from util.util import *
from service.mentor import *
import util.util

router = APIRouter(tags=["admin"], prefix="/admin")

#


@router.get("/user-roles/", response_model=List[UserRoleResponse])
async def read_user_roles(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    return db.query(UserRole).all()


@router.post("/add-user/", response_model=UserInfoResponse)
async def create_user(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    new_user: UserAddRequest,

    db: Session = Depends(get_db),
):
    new_db_user = User(
        user_type_id=new_user.user_type_id,
        fname=new_user.fname,
        lname=new_user.lname,
        father_name=new_user.father_name,
        birth=new_user.birth,

        resume_file_id=new_user.resume_file_id,
        address=new_user.address,
        username=new_user.username,
        password=new_user.password,
        phone=new_user.phone,
        active=new_user.active,
    )
    if db.query(User).filter(User.username == new_user.username).first():
        raise HTTPException(
            status_code=403, detail="username exist"
        )
    db.add(new_db_user)
    db.commit()
    db.refresh(new_db_user)
    return new_db_user


@router.put("/update-user/{user_id}", response_model=UserInfoResponse)
async def update_user(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    update_user: UserAddRequest,
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=403, detail="user dose not exists"
        )
    if update_user.user_type_id:
        user.user_type_id = update_user.user_type_id
    if update_user.fname:
        user.fname = update_user.fname
    if update_user.lname:
        user.lname = update_user.lname
    if update_user.father_name:
        user.father_name = update_user.father_name
    if update_user.birth:
        user.birth = update_user.birth
    if update_user.resume_file_id:
        user.resume_file_id = update_user.resume_file_id
    if update_user.address:
        user.address = update_user.address
    if update_user.username:
        user.username = update_user.username
    if update_user.password:
        user.password = util.util.hash(update_user.password)
    if update_user.phone:
        user.phone = update_user.phone
    if update_user.active:
        user.active = update_user.active

    db.commit()
    db.refresh(user)
    return user


@router.delete("/delete-user/{user_id}", response_model=UserInfoResponse)
async def update_user(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=403, detail="user dose not exists"
        )
    user.active = False
    db.commit()
    db.refresh(user)
    return user


@router.get("/users/", response_model=List[UserInfoResponse])
async def read_users(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    active: bool,
    skip: int = 0,
    limit: int = 10,
    fname: str = None,
    db: Session = Depends(get_db),
):
    users = admin_get_users_like(
        db=db, skip=skip, limit=limit, fname=fname, active=active)
    return users


@router.get("/logs/", response_model=List[LogResponse])
async def read_logs(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 10,

    db: Session = Depends(get_db),
):
    logs = get_logs(db, skip=skip, limit=limit)
    return logs
