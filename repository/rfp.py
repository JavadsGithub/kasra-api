from sqlalchemy.orm import Session
from model import schemas
from model.model import RFP, RFPField
from model.schemas import *
from fastapi import HTTPException


def explorer_search_rfps(db: Session, query: str, skip: int = 0, limit: int = 10):
    return (
        db.query(RFP)
        .filter(RFP.info.ilike(f"%{query}%"))
        .offset(skip)
        .limit(limit)
        .all()
    )


def explorer_get_rfps(db: Session, skip: int = 0, limit: int = 10):
    return db.query(RFP).offset(skip).limit(limit).all()


def explorer_get_rfp_fields(db: Session, skip: int = 0, limit: int = 10):
    return db.query(RFPField).offset(skip).limit(limit).all()


def explorer_create_rfp(db: Session, rfp: RFPRequest):
    new_rfp = RFP(
        info=rfp.info,
        RFP_field_id=rfp.RFP_field_id,
        file_id=rfp.file_id,
    )
    db.add(new_rfp)
    db.commit()
    db.refresh(new_rfp)
    return new_rfp


def explorer_update_rfp(db: Session, rfp_id: int, rfp_update: RFPRequest):
    rfp = db.query(RFP).filter(RFP.id == rfp_id).first()
    if not rfp:
        raise HTTPException(status_code=404, detail="RFP not found")
    if rfp_update.info is not None:
        rfp.info = rfp_update.info
    if rfp_update.file_id is not None:
        rfp.file_id = rfp_update.file_id

    db.commit()
    db.refresh(rfp)
    return rfp
