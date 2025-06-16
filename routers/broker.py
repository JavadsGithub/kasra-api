from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from datetime import time

from repository.broker import *
from util.util import *


router = APIRouter(tags=["broker"], prefix="/broker")


@router.get("/proposals/", response_model=List[ProposalResponse])
async def read_proposals(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    proposals = broker_get_proposals(db, skip=skip, limit=limit)
    return proposals


@router.get("/proposals-like/", response_model=List[ProposalResponse])
async def read_proposals(
    skip: int = 0, limit: int = 10, info: str = None, db: Session = Depends(get_db)
):
    proposals = broker_get_proposals_like(db, skip=skip, limit=limit, info=info)
    return proposals


@router.get("/proposals/{proposal_id}", response_model=ProposalResponse)
async def read_proposal(proposal_id: int, db: Session = Depends(get_db)):
    return broker_get_proposal_by_id(db=db, proposal_id=proposal_id)


@router.post("/commissions/", response_model=CommissionResponse)
async def add_commission(
    commission_request: CommissionRequest, db: Session = Depends(get_db)
):
    return broker_create_commission(db=db, commission=commission_request)
