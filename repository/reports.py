from sqlalchemy.orm import Session
from model.model import *
from model.schemas import *
from fastapi import HTTPException


def supervisor_get_reports(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Report).offset(skip).limit(limit).all()


def supervisor_get_reports_by_project(db: Session, project_id: int):
    return db.query(Report).filter(Report.project_id == project_id).all()


def supervisor_get_reports_by_id(db: Session, id: int):
    return db.query(Report).filter(Report.id == id).first()


def user_get_reports_by_project(db: Session, project_id: int):
    return db.query(Report).filter(Report.project_id == project_id).all()


# def supervisor_get_report_with_files(db: Session, report_id: int):
#     report = db.query(Report).filter(Report.id == report_id).first()
#     if not report:
#         raise HTTPException(status_code=404, detail="Report not found")

#     report_files = db.query(ReportFile).filter(ReportFile.report_id == report_id).all()
#     return report_files


def supervisor_update_report(db: Session, report_id: int, report_update: ReportUpdate):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    report.comment = report_update.comment
    report.state = report_update.state

    db.commit()
    db.refresh(report)
    return report


def mentor_get_report(db: Session, project_id: int, skip: int, limit: int):
    return (
        db.query(Report)
        .filter(Report.project_id == project_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def mentor_get_all_report(db: Session, skip: int, limit: int):
    return db.query(Report).offset(skip).limit(limit).all()
