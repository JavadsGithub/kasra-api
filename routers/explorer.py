from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from repository.allocate import explorer_allocate_single, explorer_search_allocate, explorer_update_allocate
from repository.proposal import explorer_get_proposals_like, explorer_update_proposal
from repository.user import explorer_get_users_supervisor
from service import explorer
from service.explorer import rfps_exist
from model import model
from model.schemas import *
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from sqlalchemy import update, desc
from datetime import time

from repository.rfp import *
from util.util import *


router = APIRouter(tags=["explorer"], prefix="/explorer")


@router.get("/rfp-fields/", response_model=List[RFPFieldResponse])
async def read_rfp_fields(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    rfp_fields = explorer_get_rfp_fields(db, skip=skip, limit=limit)
    rfps_exist(rfp_fields)
    return rfp_fields


@router.get("/rfps/", response_model=List[RFPResponse])
async def search_rfps_endpoint(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    info: str = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    rfps = explorer_search_rfps(db, info=info, skip=skip, limit=limit)
    rfps_exist(rfps)
    return rfps


@router.get("/single-rfp/{rfp_id}", response_model=RFPResponse)
async def search_rfps(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    rfp_id: int,
    db: Session = Depends(get_db),
):
    rfp = explorer_rfp_single(db, rfp_id=rfp_id)
    rfps_exist(rfp)
    return rfp


@router.post("/rfps/", response_model=RFPResponse)
async def add_rfp(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    rfp: ExplorerCreateUpdateRFP,
    db: Session = Depends(get_db),
):
    return explorer_create_rfp(db=db, rfp=rfp, creator_id=current_user.id)


@router.put("/rfps/{rfp_id}", response_model=RFPResponse)
async def edit_rfp(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    rfp_id: int,
    rfp_update: ExplorerCreateUpdateRFP,
    db: Session = Depends(get_db),
):
    return explorer_update_rfp(db=db, rfp_id=rfp_id, rfp_update=rfp_update)


@router.get("/users-supervisor/", response_model=List[UserInfoResponse])
async def read_users_supervisor(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    users = explorer_get_users_supervisor(db)
    return users

# Proposal-like:


@router.get("/proposals/", response_model=List[ProposalResponse])
async def read_proposals(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 10,
    info: str = None,
    db: Session = Depends(get_db),
):
    proposals = explorer_get_proposals_like(
        db, skip=skip, limit=limit, info=info, creator_id=current_user.id)
    return proposals


@router.put("/proposal/{proposal_id}", response_model=ProposalResponse)
async def edit_proposal(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    proposal_id: int,
    proposal_update: ExplorerUpdateProposal,
    db: Session = Depends(get_db),
):
    return explorer_update_proposal(
        db=db, proposal_id=proposal_id, proposal_update=proposal_update
    )


@router.put("/allocates/{allocate_id}", response_model=AllocateResponse)
async def edit_allocate(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    allocate_id: int,
    allocate_update: BrokerUpdateAllocate,
    db: Session = Depends(get_db),
):
    return explorer_update_allocate(db=db, allocate_update=allocate_update, allocate_id=allocate_id)


@router.get("/allocates/", response_model=List[AllocateResponse])
async def get_allocates(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    allocate = explorer_search_allocate(
        db, creator_id=current_user.id, skip=skip, limit=limit)
    if not allocate:
        raise HTTPException(status_code=404, detail="No allocate found")
    return allocate


@router.get("/single-allocate/{allocate_id}", response_model=AllocateResponse)
async def single_allocate(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    allocate_id: int,
    db: Session = Depends(get_db),
):
    allocate = explorer_allocate_single(db, allocate_id=allocate_id)
    if not allocate:
        raise HTTPException(status_code=404, detail="No allocate found")
    return allocate
