from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model, schemas
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from sqlalchemy import update, desc
from datetime import time
from repository.proposal import *
from repository.projects import *
from repository.reports import *
from service.user import reports_exist
from util.util import *


router = APIRouter(tags=["supervisor"], prefix="/supervisor")


# @router.get("/proposals/", response_model=List[ProposalResponse])
# async def read_proposals(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     proposals = suoervisor_get_proposals(db, skip=skip, limit=limit)
#     return proposals


@router.get("/proposals/", response_model=List[ProposalResponse])
async def read_proposals(
    skip: int = 0, limit: int = 10, info: str = None, db: Session = Depends(get_db)
):
    proposals = suoervisor_get_proposals_like(db, skip=skip, limit=limit, info=info)
    return proposals


@router.get("/proposals/{proposal_id}", response_model=ProposalResponse)
async def read_proposal(proposal_id: int, db: Session = Depends(get_db)):
    return suoervisor_get_proposal_by_id(db=db, proposal_id=proposal_id)


@router.get("/reports-by-project/{project_id}", response_model=List[ReportResponse])
async def read_reports_by_project(project_id: int, db: Session = Depends(get_db)):
    reports = supervisor_get_reports_by_project(db, project_id=project_id)
    if not reports:
        return []
    return reports


@router.get("/single-report/{id}", response_model=ReportResponse)
async def read_reports_by_project(id: int, db: Session = Depends(get_db)):
    report = supervisor_get_reports_by_id(db, id=id)
    if not report:
        raise HTTPException(status_code=404, detail="No Reports found")
    return report


@router.get("/reports/", response_model=List[ReportResponse])
async def read_reports(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reports = supervisor_get_reports(db, skip=skip, limit=limit)
    return reports


# @router.get("/report-files/{report_id}", response_model=List[ReportFileResponse])
# async def read_report(report_id: int, db: Session = Depends(get_db)):
#     return supervisor_get_report_with_files(db=db, report_id=report_id)


@router.put("/reports/{report_id}", response_model=ReportResponse)
async def edit_report(
    report_id: int, report_update: ReportUpdate, db: Session = Depends(get_db)
):
    return supervisor_update_report(
        db=db, report_id=report_id, report_update=report_update
    )


@router.get("/projects/", response_model=List[ProjectResponse])
async def read_projects(
    skip: int = 0, limit: int = 10, info: str = None, db: Session = Depends(get_db)
):
    projects = supervisor_get_projects(db, skip=skip, limit=limit, info=info)
    return projects


@router.get("/single-project/{project_id}", response_model=ProjectResponse)
async def read_projects(project_id: int, db: Session = Depends(get_db)):
    projects = supervisor_get_single_project(db=db, project_id=project_id)
    if not projects:
        raise HTTPException(status_code=404, detail="No Projects found")
    return projects
