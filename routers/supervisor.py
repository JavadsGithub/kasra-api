from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model, schemas
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from sqlalchemy import update, desc
from datetime import time
from repository.supervisor import *
from util.util import *


router = APIRouter(tags=["supervisor"], prefix="/supervisor")


@router.get("/proposals/", response_model=List[Proposal])
async def read_proposals(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    proposals = get_proposals(db, skip=skip, limit=limit)
    return proposals


@router.get("/proposals/", response_model=List[Proposal])
async def read_proposals(
    skip: int = 0, limit: int = 10, info: str = None, db: Session = Depends(get_db)
):
    proposals = get_proposals(db, skip=skip, limit=limit, info=info)
    return proposals


@router.get("/proposals/{proposal_id}", response_model=Proposal)
async def read_proposal(proposal_id: int, db: Session = Depends(get_db)):
    return get_proposal_by_id(db=db, proposal_id=proposal_id)


@router.put("/proposals/{proposal_id}", response_model=ProposalResponse)
async def edit_proposal(
    proposal_id: int, proposal_update: ProposalUpdate, db: Session = Depends(get_db)
):
    return update_proposal(
        db=db, proposal_id=proposal_id, proposal_update=proposal_update
    )


@router.get("/reports/", response_model=List[Report])
async def read_reports(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reports = get_reports(db, skip=skip, limit=limit)
    return reports


@router.get("/reports/{report_id}", response_model=dict)
async def read_report(report_id: int, db: Session = Depends(get_db)):
    return get_report_with_files(db=db, report_id=report_id)


@router.put("/reports/{report_id}", response_model=ReportResponse)
async def edit_report(
    report_id: int, report_update: ReportUpdate, db: Session = Depends(get_db)
):
    return update_report(db=db, report_id=report_id, report_update=report_update)


@router.get("/projects/", response_model=List[Project])
async def read_projects(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    projects = get_projects(db, skip=skip, limit=limit)
    return projects
