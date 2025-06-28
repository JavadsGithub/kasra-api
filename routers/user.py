from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from datetime import time
import datetime
from repository.user import *
from util.util import *
from util import util

router = APIRouter(tags=["user"], prefix="/users")


@router.get("/seed/")
async def add_proposal(db: Session = Depends(get_db)
):
    db = database.SessionLocal()

    new_user_roules = [
        UserRole(title="کارگزار"),
        UserRole(title="کاشف"),
        UserRole(title="کاربر"),
        UserRole(title="ناظر"),
        UserRole(title="استاد راهنما"),
    ]
    db.add_all(new_user_roules)
    db.commit()
    new_file = File(info="file.pdf", access_id=1)
    db.add(new_file)
    db.commit()

    rolese = db.query(UserRole).all()
    my_file = db.query(File).first()
    file_i = my_file.id
    new_users = [
        User(
            user_type_id=rolese[0].id,
            fname="جواد",
            lname="جوادی",
            father_name="محمدجواد",
            resume_file_id=file_i,
            birth=datetime.now(),
            address="همدان-جوادیه",
            username="admin",
            password=util.hash("admin"),
            phone="09181020300",
            active=True,
        ),
        User(
            user_type_id=rolese[1].id,
            fname="علی",
            lname="اکبری",
            father_name="حسن",
            birth=datetime.now(),
            resume_file_id=file_i,
            address="تهران-اکبرآباد",
            username="admin2",
            password=util.hash("admin"),
            phone="09182020301",
            active=True,
        ),
        User(
            user_type_id=rolese[2].id,
            fname="سارا",
            lname="موسوی",
            father_name="محمد",
            birth=datetime.now(),
            resume_file_id=file_i,
            address="اصفهان-موسوی",
            username="admin3",
            password=util.hash("admin"),
            phone="09183020302",
            active=True,
        ),
        User(
            user_type_id=rolese[3].id,
            fname="زهرا",
            lname="حسینی",
            father_name="علی",
            birth=datetime.now(),
            resume_file_id=file_i,
            address="شیراز-حسینیه",
            username="admin4",
            password=util.hash("admin"),
            phone="09184020303",
            active=True,
        ),
        User(
            user_type_id=rolese[4].id,
            fname="رضا",
            lname="نیکو",
            father_name="سید",
            birth=datetime.now(),
            resume_file_id=file_i,
            address="مشهد-رضوی",
            username="admin5",
            password=util.hash("admin"),
            phone="09185020304",
            active=True,
        ),
    ]
    db.add_all(new_users)
    db.commit()

    return {"response":"ok"}


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
