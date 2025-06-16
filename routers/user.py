from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from datetime import time

from repository.user import *
from util.util import *


router = APIRouter(tags=["user"], prefix="/users")


@router.post("/proposals/", response_model=ProposalResponse)
async def add_proposal(
    proposal_request: ProposalRequest, db: Session = Depends(get_db)
):
    return user_create_proposal(db=db, proposal=proposal_request)


@router.get("/proposals/{proposal_id}", response_model=ProposalResponse)
async def read_proposal(proposal_id: int, db: Session = Depends(get_db)):
    return user_get_proposal_by_id(db=db, proposal_id=proposal_id)


@router.get("/projects/", response_model=List[ProjectResponse])
async def read_projects(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    user_id = 0
    projects = user_get_projects(db, skip=skip, limit=limit, user_id=user_id)
    return projects


@router.get("/reports-by-project/{project_id}", response_model=List[ReportResponse])
async def read_reports(project_id: int, db: Session = Depends(get_db)):
    reports = user_get_reports_by_project(db, project_id)
    if not reports:
        raise HTTPException(status_code=404, detail="Reports not found")
    return reports


@router.post("/reports/", response_model=ReportResponse)
async def add_report(report_request: ReportRequest, db: Session = Depends(get_db)):
    return user_create_report(db=db, report=report_request)


@router.get("/reports/{report_id}", response_model=ReportResponse)
async def read_report(report_id: int, db: Session = Depends(get_db)):
    return user_get_report_by_id(db=db, report_id=report_id)
