from sqlalchemy.sql import exists
from sqlalchemy.orm import Session
from model.model import *
from model.schemas import *
from fastapi import HTTPException


def get_proposals(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Proposal).offset(skip).limit(limit).all()


def get_proposals(db: Session, skip: int = 0, limit: int = 10, info: str = None):
    query = db.query(Proposal)

    if info:
        query = query.filter(Proposal.info.ilike(f"%{info}%"))
    return query.offset(skip).limit(limit).all()


def get_proposal_by_id(db: Session, proposal_id: int):
    proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return proposal


def update_proposal(db: Session, proposal_id: int, proposal_update: ProposalUpdate):
    proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    proposal.state = proposal_update.state
    proposal.comment = proposal_update.comment

    db.commit()
    db.refresh(proposal)
    return proposal


def get_reports(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Report).offset(skip).limit(limit).all()


def get_report_with_files(db: Session, report_id: int):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    report_files = db.query(ReportFile).filter(ReportFile.report_id == report_id).all()
    return {"report": report, "files": report_files}


def update_report(db: Session, report_id: int, report_update: ReportUpdate):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    report.comment = report_update.comment
    report.state = report_update.state

    db.commit()
    db.refresh(report)
    return report


def get_projects(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Project).offset(skip).limit(limit).all()
