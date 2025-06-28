from sqlalchemy.orm import Session
from model.model import *
from model.schemas import *
from fastapi import HTTPException


def suoervisor_get_reports(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Report).offset(skip).limit(limit).all()


def suoervisor_get_report_with_files(db: Session, report_id: int):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    report_files = db.query(ReportFile).filter(ReportFile.report_id == report_id).all()
    return {"report": report, "files": report_files}


def suoervisor_update_report(db: Session, report_id: int, report_update: ReportUpdate):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    report.comment = report_update.comment
    report.state = report_update.state

    db.commit()
    db.refresh(report)
    return report
