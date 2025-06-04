from datetime import datetime
from sqlalchemy.orm import Session
from model.model import *
from model.schemas import *
from fastapi import HTTPException


def create_proposal(db: Session, proposal: ProposalRequest):
    db_proposal = Proposal(
        info=proposal.info,
        RFP_id=proposal.RFP_id,
        user_id=proposal.user_id,
        file_id=proposal.file_id,
        state=proposal.state,
        comment=proposal.comment,
    )
    db.add(db_proposal)
    db.commit()
    db.refresh(db_proposal)
    return db_proposal


def get_proposal_by_id(db: Session, proposal_id: int):
    proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return proposal


def get_projects(
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


def get_reports_by_project(db: Session, project_id: int):
    return db.query(Report).filter(Report.project_id == project_id).all()


def create_report(db: Session, report: ReportRequest):
    db_report = Report(
        info=report.info,
        project_id=report.project_id,
        comment=report.comment,
        state=report.state,
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


def get_report_by_id(db: Session, report_id: int):
    report = db.query(Report).filter(Report.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report
