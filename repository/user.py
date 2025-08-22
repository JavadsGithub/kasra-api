from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, or_
from model.model import *
from model.schemas import *
from fastapi import HTTPException
from datetime import datetime


# def user_create_proposal(db: Session, proposal: ProposalRequest, user_id: int):
#     db_proposal = Proposal(
#         info=proposal.info,
#         RFP_id=proposal.RFP_id,
#         user_id=user_id,
#         file_id=proposal.file_id,
#         state=3,
#         comment=proposal.comment,
#     )
#     db.add(db_proposal)
#     db.commit()
#     db.refresh(db_proposal)
#     return db_proposal


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
        db.query(Project).order_by(Project.id.desc())
        .filter(Project.user_user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def user_get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()


def user_create_report(db: Session, creator_id: int, report: ReportRequest):
    db_report = Report(
        creator_id=creator_id,
        created_at=datetime.now(),
        title=report.title,
        project_id=report.project_id,
        comment="",
        file_pdf_id=report.file_pdf_id,
        file_docx_id=report.file_docx_id,
        file_pptx_id=report.file_pptx_id,
        anounced_percent=report.anounced_percent,
        accepted_percent=0,
        state=ReportState.pending,
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
    # query = db.query(User).join(Allocate).order_by(Proposal.id.desc())
    # users = db.query(Allocate).filter(
    #     (Allocate.allocated_to_user == User.id)
    #     & (Allocate.state != AllocatetState.pending_to_specify_title)
    #     & (User.user_type_id == 3)).all()
    users = (
        db.query(User)
        .outerjoin(Allocate, User.id == Allocate.allocated_to_user_id)
        # .filter(Allocate.state != AllocatetState.pending_to_specify_title,)
        .filter(or_(

                Allocate.id.is_(None),  # برای کاربرانی که Allocate ندارند
                Allocate.state != AllocatetState.pending_to_specify_title,
                ))
        .filter(User.user_type_id == 3)

        .group_by(User.id)
        .having(func.count(Allocate.id) < 2)
        .all()
    )
    return users
    # return db.query(User).filter(User.user_type_id == 3)


def broker_get_users_discoverer(db: Session):
    return db.query(User).filter(User.user_type_id == 1)


def explorer_get_users_supervisor(db: Session):
    return db.query(User).filter(User.user_type_id == 4)


def create_notif(db: Session, user_id: int, title: str):
    new_notif = Notification(
        owner=user_id,
        created_at=datetime.now(),
        title=title,
        seen=False
    )
    db.add(new_notif)
    db.commit()
# create_notif(db=db, user_id=user_id, title="")


def admin_get_users_like(
    db: Session, skip: int = 0, limit: int = 10, fname: str = None
):
    query = db.query(User).order_by(User.id.desc())
    if fname:
        query = query.filter(User.lname.ilike(
            f"%{fname}%"))
    return query.offset(skip).limit(limit).all()


def researcher_get_masters_like(
    db: Session, skip: int = 0, limit: int = 10, name: str = None
):
    query = db.query(Master).order_by(Master.id.desc())
    if name:
        query = query.filter(Master.name.ilike(
            f"%{name}%"))
    return query.offset(skip).limit(limit).all()
