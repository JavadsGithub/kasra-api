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
        file_id=commission.file_id,
    )
    db.add(db_commission)
    db.commit()
    db.refresh(db_commission)
    return db_commission
