from sqlalchemy.orm import Session
from model.model import *
from model.schemas import *
from fastapi import HTTPException

from routers import file


def supervisor_get_reports(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Report).order_by(Report.id.desc()).offset(skip).limit(limit).all()


def supervisor_get_reports_by_project(db: Session, project_id: int):
    return db.query(Report).order_by(Report.id.desc()).filter(Report.project_id == project_id).all()


def supervisor_get_reports_by_id(db: Session, id: int):
    return db.query(Report).filter(Report.id == id).first()


def user_get_reports_by_project(db: Session, project_id: int, creator_id: int):
    return db.query(Report).order_by(Report.id.desc()).filter(
        (Report.project_id == project_id) & (Report.creator_id == creator_id)
    ).all()


# def supervisor_get_report_with_files(db: Session, report_id: int):
#     report = db.query(Report).filter(Report.id == report_id).first()
#     if not report:
#         raise HTTPException(status_code=404, detail="Report not found")

#     report_files = db.query(ReportFile).filter(ReportFile.report_id == report_id).all()
#     return report_files


def supervisor_accept_report(db: Session, report_id: int, report_update: ReportUpdate, file_id: int):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if file_id != 0:
        report.supervisor_file_id = file_id
    report.comment = report_update.comment

    report.state = ReportState.eccepted
    # if report_update.state == ReportState.eccepted:
    report.accepted_percent = report_update.accepted_percent
    project = db.query(Project).filter(
        Project.id == report.project_id).first()
    if not project:
        raise HTTPException(
            status_code=404, detail="the project not found")
    if report_update.commission_date_time:
        project.commission_date_time = report_update.commission_date_time

    project.accepted_percent = report_update.accepted_percent

    db.commit()
    db.refresh(report)
    return report


def supervisor_reject_report(db: Session, report_id: int, report_update: ReportUpdate, file_id: int):
    report = db.query(Report).filter(Report.id == report_id).first()
    if file_id != 0:
        report.supervisor_file_id = file_id
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    report.comment = report_update.comment
    report.state = ReportState.rejected
    db.commit()
    db.refresh(report)
    return report


def researcher_get_report(db: Session, project_id: int, skip: int, limit: int):
    return (
        db.query(Report).order_by(Report.id.desc())
        .filter(Report.project_id == project_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def researcher_get_one_report(db: Session, report_id: int):
    return (
        db.query(Report)
        .filter(Report.id == report_id)
        .first()
    )


def researcher_get_all_report(db: Session, skip: int, limit: int):
    return db.query(Report).offset(skip).limit(limit).all()
