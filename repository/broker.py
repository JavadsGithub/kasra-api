from datetime import datetime
from sqlalchemy.orm import Session
from model.model import *
from model.schemas import *
from fastapi import HTTPException


def broker_get_proposals(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Proposal).offset(skip).limit(limit).all()


def broker_get_proposals_like(
    db: Session, skip: int = 0, limit: int = 10, info: str = None
):
    query = db.query(Proposal)

    if info:
        query = query.filter(Proposal.info.ilike(f"%{info}%"))
    return query.offset(skip).limit(limit).all()


def broker_get_proposal_by_id(db: Session, proposal_id: int):
    proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return proposal


# ..................
def broker_create_commission(db: Session, commission: CommissionRequest):
    db_commission = Commission(
        title=commission.title,
        comment=commission.comment,
        state=commission.state,
        proposal_id=commission.proposal_id,
        user_supervisor_id=commission.user_supervisor_id,
        user_discoverer_id=commission.user_discoverer_id,
        file_id=commission.file_id,
    )
    db.add(db_commission)
    db.commit()
    db.refresh(db_commission)
    return db_commission
