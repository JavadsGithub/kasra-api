from sqlalchemy.sql import exists
from sqlalchemy.orm import Session
from model import model, schemas
from model.schemas import *
from fastapi import HTTPException


def search_rfps(db: Session, query: str, skip: int = 0, limit: int = 10):
    return (
        db.query(schemas.RFPResponse)
        .filter(schemas.RFPResponse.info.ilike(f"%{query}%"))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_rfps(db: Session, skip: int = 0, limit: int = 10):
    return db.query(schemas.RFPResponse).offset(skip).limit(limit).all()


def create_rfp(db: Session, rfp: RFPRequest):
    new_rfp = RFPResponse(rfp)
    db.add(new_rfp)
    db.commit()
    db.refresh(new_rfp)
    return new_rfp


def update_rfp(db: Session, rfp_id: int, rfp_update: RFPRequest):
    rfp = db.query(RFPResponse).filter(RFPResponse.id == rfp_id).first()
    if not rfp:
        raise HTTPException(status_code=404, detail="RFP not found")

    if rfp_update.info is not None:
        rfp.info = rfp_update.info
    if rfp_update.file_id is not None:
        rfp.file_id = rfp_update.file_id

    db.commit()
    db.refresh(rfp)
    return rfp
