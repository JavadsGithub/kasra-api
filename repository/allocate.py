from sqlalchemy.orm import Session
from model import schemas
from model.model import RFP, Allocate, AllocatetState, RFPField
from model.schemas import *
from fastapi import HTTPException
from datetime import datetime

from repository.user import create_notif


def broker_create_allocate(db: Session, allocate: BrokerCreateAllocate, creator_id: int):
    new_rfp = Allocate(
        RFP_id=allocate.RFP_id,
        allocated_to_user_id=allocate.allocated_to_user_id,
        creator_id=creator_id,
        created_at=datetime.now(),
        state=AllocatetState.pending_to_specify_title
    )
    db.add(new_rfp)
    db.commit()
    db.refresh(new_rfp)
    return new_rfp


def broker_search_allocate(creator_id: int, db: Session, skip: int = 0, limit: int = 10):
    query = db.query(Allocate).order_by(Allocate.id.desc())
    # query = query.filter(Allocate.state == AllocatetState.pending_to_accept)
    return query.offset(skip).limit(limit).all()


def broker_allocate_single(db: Session, allocate_id: int):
    return db.query(Allocate).filter(Allocate.id == allocate_id).first()


# SUS
def explorer_search_allocate(creator_id: int, db: Session, skip: int = 0, limit: int = 10):
    query = db.query(Allocate).join(RFP).order_by(Allocate.id.desc())
    query = query.filter(RFP.creator_id == creator_id)
    return query.offset(skip).limit(limit).all()


def explorer_allocate_single(db: Session, allocate_id: int):
    return db.query(Allocate).filter(Allocate.id == allocate_id).first()


def explorer_update_allocate(
    db: Session, allocate_id: int, allocate_update: BrokerUpdateAllocate
):
    allocate = db.query(Allocate).filter(Allocate.id == allocate_id).first()
    if not allocate:
        raise HTTPException(status_code=404, detail="allocate not found")

    allocate.state = AllocatetState.eccepted
    allocate.master = allocate_update.supervisor_id

    db.commit()
    db.refresh(allocate)
    return allocate


def researcher_accept_allocate(
    db: Session, allocate_id: int
):
    allocate = db.query(Allocate).filter(Allocate.id == allocate_id).first()
    if not allocate:
        raise HTTPException(status_code=404, detail="allocate not found")
    create_notif(db=db, user_id=allocate.allocated_to_user_id,
                 title="موضوع پروژه شما تایید شد و در انتطار ویرایش پروپوزال میباشد")
    allocate.state = AllocatetState.eccepted

    db.commit()
    db.refresh(allocate)
    return allocate


def researcher_reject_allocate(
    db: Session, allocate_id: int
):
    allocate = db.query(Allocate).filter(Allocate.id == allocate_id).first()
    if not allocate:
        raise HTTPException(status_code=404, detail="allocate not found")

    allocate.state = AllocatetState.rejected

    db.commit()
    db.refresh(allocate)
    return allocate


def user_search_allocate(user_id: int, db: Session, skip: int = 0, limit: int = 10):
    query = db.query(Allocate)
    query = query.filter(Allocate.allocated_to_user_id == user_id)
    return query.offset(skip).limit(limit).all()


def user_allocate_single(db: Session, allocate_id: int):
    return db.query(Allocate).filter(Allocate.id == allocate_id).first()


def user_update_allocate(
    db: Session, allocate_id: int, allocate_update: UserUpdateAllocate
):
    allocate = db.query(Allocate).filter(Allocate.id == allocate_id).first()
    if not allocate:
        raise HTTPException(status_code=404, detail="allocate not found")

    allocate.state = AllocatetState.pending_to_specify_supervisor
    allocate.project_title = allocate_update.project_title
    allocate.project_description = allocate_update.project_description

    db.commit()
    db.refresh(allocate)
    return allocate
