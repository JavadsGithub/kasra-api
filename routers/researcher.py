from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model, schemas
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from sqlalchemy import update, desc
from datetime import time

from repository.allocate import broker_allocate_single, broker_search_allocate, researcher_accept_allocate, researcher_reject_allocate
from repository.projects import *
from repository.reports import *
from model.schemas import *
from util.util import *
from service.mentor import *

router = APIRouter(tags=["researcher"], prefix="/researcher")


@router.get("/projects/", response_model=List[ProjectResponse])
async def get_project(
    current_user: Annotated[UserInfoResponse, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    user_id = current_user.id
    projects = researcher_get_projects(
        db, user_id=user_id, skip=skip, limit=limit)
    return projects


@router.get("/reports/{project_id}")
async def get_reports(
    current_user: Annotated[UserInfoResponse, Depends(get_current_user)],
    project_id: int = 0,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):

    return researcher_get_report(db, project_id=project_id, skip=skip, limit=limit)


@router.get("/single-report/{report_id}")
async def get_single_reports(
    current_user: Annotated[UserInfoResponse, Depends(get_current_user)],
    report_id: int = 0,
    db: Session = Depends(get_db),
):
    return researcher_get_one_report(db, report_id=report_id,)


@router.get("/all-reports/")
async def get_all_reports(
    current_user: Annotated[UserInfoResponse, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):

    return researcher_get_all_report(db, skip=skip, limit=limit)
# OLD ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^6


@router.put("/allocates/{allocate_id}", response_model=AllocateResponse)
async def edit_allocate(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    allocate_id: int,
    accept: bool = False,
    db: Session = Depends(get_db),
):
    if accept:
        return researcher_accept_allocate(db=db, allocate_id=allocate_id)
    else:
        return researcher_reject_allocate(db=db, allocate_id=allocate_id)


@router.get("/allocates/", response_model=List[AllocateResponse])
async def get_allocates(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    allocate = broker_search_allocate(
        db, creator_id=current_user.id, skip=skip, limit=limit)
    if not allocate:
        raise HTTPException(status_code=404, detail="No allocate found")
    return allocate


@router.get("/single-allocate/{allocate_id}", response_model=AllocateResponse)
async def single_allocate(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    allocate_id: int,
    db: Session = Depends(get_db),
):
    allocate = broker_allocate_single(db, allocate_id=allocate_id)
    if not allocate:
        raise HTTPException(status_code=404, detail="No allocate found")
    return allocate


@router.put("/projects/{project_id}", response_model=AllocateResponse)
async def edit_accepting_project(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    project_id: int,
    db: Session = Depends(get_db),
):
    return researcher_accept_project(db=db, project_id=project_id)
