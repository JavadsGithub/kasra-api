from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model, schemas
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from sqlalchemy import update, desc
from datetime import time

from repository.projects import *
from repository.reports import *
from model.schemas import *
from util.util import *
from service.mentor import *

router = APIRouter(tags=["mentor"], prefix="/mentor")


@router.get("/projects/", response_model=List[ProjectResponse])
async def get_project(
    current_user: Annotated[UserInfoResponse, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    # if not current_user.user_type_id == 5:
    #     raise HTTPException(status_code=401, detail="Not Allowed")

    user_id = current_user.id
    projects = mentor_get_projects(db, user_id=user_id, skip=skip, limit=limit)
    return projects


@router.get("/reports/{project_id}")
async def get_reports(
    current_user: Annotated[UserInfoResponse, Depends(get_current_user)],
    project_id: int = 0,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):

    return mentor_get_report(db, project_id=project_id, skip=skip, limit=limit)
