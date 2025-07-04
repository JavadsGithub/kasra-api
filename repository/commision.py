from sqlalchemy.orm import Session
from model.model import *
from model.schemas import *
from fastapi import HTTPException


# ..................
def broker_create_commission(db: Session, commission: CommissionRequest):
    db_commission = Commission(
        title=commission.title,
        comment=commission.comment,
        state=commission.state,
        proposal_id=commission.proposal_id,
        user_supervisor_id=commission.user_supervisor_id,
        user_discoverer_id=commission.user_discoverer_id,
        user_master_id=commission.user_master_id,
    )
    db.add(db_commission)
    db.commit()
    db.refresh(db_commission)
    return db_commission


def broker_get_commission(db: Session, proposal_id: int):
    commission = (
        db.query(Commission).filter(Commission.proposal_id == proposal_id).first()
    )
    return commission
