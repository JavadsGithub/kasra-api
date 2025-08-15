from sqlalchemy.orm import Session
from model import schemas
from model.model import RFP, RFPField
from model.schemas import *
from fastapi import HTTPException
from datetime import datetime


def explorer_search_rfps(db: Session, skip: int = 0, limit: int = 10, info: str = None):
    query = db.query(RFP).order_by(RFP.id.desc())
    if info:
        query = query.filter(RFP.info.ilike(f"%{info}%"))
    return query.offset(skip).limit(limit).all()


def user_search_rfps(db: Session, skip: int = 0, limit: int = 10, info: str = None):
    query = db.query(RFP).order_by(RFP.id.desc())
    if info:
        query = query.filter(RFP.info.ilike(f"%{info}%"))
    return query.offset(skip).limit(limit).all()


def explorer_rfp_single(db: Session, rfp_id: int):
    return db.query(RFP).filter(RFP.id == rfp_id).first()


def explorer_get_rfps(db: Session, skip: int = 0, limit: int = 10):
    return db.query(RFP).order_by(RFP.id.desc()).offset(skip).limit(limit).all()


def explorer_get_rfp_fields(db: Session, skip: int = 0, limit: int = 10):
    return db.query(RFPField).offset(skip).limit(limit).all()


def explorer_create_rfp(db: Session, rfp: ExplorerCreateUpdateRFP, creator_id: int):
    new_rfp = RFP(
        info=rfp.info,
        RFP_field_id=rfp.RFP_field_id,
        file_id=rfp.file_id,
        creator_id=creator_id,
        created_at=datetime.now()
    )
    db.add(new_rfp)
    db.commit()
    db.refresh(new_rfp)
    return new_rfp


def explorer_update_rfp(db: Session, rfp_id: int, rfp_update: ExplorerCreateUpdateRFP):
    rfp = db.query(RFP).filter(RFP.id == rfp_id).first()
    if not rfp:
        raise HTTPException(status_code=404, detail="RFP not found")
    if rfp_update.info is not None:
        rfp.info = rfp_update.info
    if rfp_update.file_id is not None:
        rfp.file_id = rfp_update.file_id
    if rfp_update.RFP_field_id is not None:
        rfp.RFP_field_id = rfp_update.RFP_field_id
    db.commit()
    db.refresh(rfp)
    return rfp


def broker_get_rfp_by_id(db: Session, rfp_id: int):
    return db.query(RFP).filter(RFP.id == rfp_id).first()
