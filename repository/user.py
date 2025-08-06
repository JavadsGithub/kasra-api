from datetime import datetime
from sqlalchemy.orm import Session
from model.model import *
from model.schemas import *
from fastapi import HTTPException


def user_create_proposal(db: Session, proposal: ProposalRequest, user_id: int):
    db_proposal = Proposal(
        info=proposal.info,
        RFP_id=proposal.RFP_id,
        user_id=user_id,
        file_id=proposal.file_id,
        state=3,
        comment=proposal.comment,
    )
    db.add(db_proposal)
    db.commit()
    db.refresh(db_proposal)
    return db_proposal


def user_get_proposal_by_id(db: Session, proposal_id: int):
    proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return proposal


def user_get_projects(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 10,
):

    return (
        db.query(Project)
        .filter(Project.user_user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def user_get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()


def user_create_report(db: Session, report: ReportRequest):
    db_report = Report(
        info=report.info,
        project_id=report.project_id,
        comment=report.comment,
        file_pdf_id = report.file_pdf_id,
        file_docx_id = report.file_docx_id,
        file_pptx_id = report.file_pptx_id,
        percent = report.percent,
        state=3,
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


def user_get_report_by_id(db: Session, report_id: int):
    report = db.query(Report).filter(Report.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


def broker_get_users_master(db: Session):
    return db.query(User).filter(User.user_type_id == 4)


def broker_get_users_discoverer(db: Session):
    return db.query(User).filter(User.user_type_id == 1)


def broker_get_users_supervisor(db: Session):
    return db.query(User).filter(User.user_type_id == 3)
