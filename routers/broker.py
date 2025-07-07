from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from datetime import time

from repository.proposal import *
from repository.commision import *
from repository.projects import *
from repository.user import *
from util.util import *


router = APIRouter(tags=["broker"], prefix="/broker")


# @router.get("/proposals/", response_model=List[ProposalResponse])
# async def read_proposals(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     proposals = broker_get_proposals(db, skip=skip, limit=limit)
#     return proposals


# Proposal-like:
@router.get("/proposals/", response_model=List[ProposalResponse])
async def read_proposals(
    skip: int = 0, limit: int = 10, info: str = None, db: Session = Depends(get_db)
):
    proposals = broker_get_proposals_like(db, skip=skip, limit=limit, info=info)
    return proposals


@router.get("/proposals/{proposal_id}", response_model=ProposalResponse)
async def read_proposal(proposal_id: int, db: Session = Depends(get_db)):
    return broker_get_proposal_by_id(db=db, proposal_id=proposal_id)


@router.post("/commissions/", response_model=ProposalResponse)
async def add_commission(
    current_user: Annotated[UserInfoResponse, Depends(get_current_user)],
    commission_request: CommissionRequest,
    db: Session = Depends(get_db),
):
    proposal = broker_get_proposal_by_id(
        db=db, proposal_id=commission_request.proposal_id
    )
    new_project = Project(
        title=proposal.info,
        proposal_id=commission_request.proposal_id,
        user_supervisor_id=commission_request.user_supervisor_id,
        user_discoverer_id=commission_request.user_discoverer_id,
        user_master_id=commission_request.user_master_id,
        user_broker_id=current_user.id,
        user_user_id=proposal.id,
    )

    broker_create_project(db=db, new_project=new_project)
    broker_update_proposal(db=db, proposal_id=commission_request.proposal_id)
    return broker_create_commission(db=db, commission=commission_request)


@router.get("/commissions/", response_model=CommissionResponse)
async def add_commission(proposal_id: int, db: Session = Depends(get_db)):
    return broker_get_commission(db=db, proposal_id=proposal_id)


@router.get("/users-master/", response_model=List[UserInfoResponse])
async def read_users_master(db: Session = Depends(get_db)):
    users = broker_get_users_master(db)
    return users


@router.get("/users-discoverer/", response_model=List[UserInfoResponse])
async def read_users_discoverer(db: Session = Depends(get_db)):
    users = broker_get_users_discoverer(db)
    return users


@router.get("/users-supervisor/", response_model=List[UserInfoResponse])
async def read_users_supervisor(db: Session = Depends(get_db)):
    users = broker_get_users_supervisor(db)
    return users
