from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from datetime import time

from repository.allocate import broker_allocate_single, broker_create_allocate, broker_search_allocate
from repository.log import add_log
from repository.proposal import *
from repository.projects import *
from repository.user import *
from repository.rfp import *
from service.explorer import rfps_exist
from util.util import *

# BROKER, EXPLORER, ORDENARYUSER, SPUERVIOR, MENTOR = (
#     1,
#     2,
#     3,
#     4,
#     5,
# )


router = APIRouter(tags=["broker"], prefix="/broker")

#


@router.get("/rfps/", response_model=List[RFPResponse])
async def search_rfps_endpoint(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    info: str = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    rfps = explorer_search_rfps(db, info=info, skip=skip, limit=limit)
    # rfps_exist(rfps)
    return rfps

#


@router.get("/single-rfp/{rfp_id}", response_model=RFPResponse)
async def search_rfps(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    rfp_id: int,
    db: Session = Depends(get_db),
):
    rfp = explorer_rfp_single(db, rfp_id=rfp_id)
    # rfps_exist(rfp)
    return rfp

#
#  ///////////////////////////////////////////////


@router.post("/allocates/", response_model=AllocateResponse)
async def add_allocate(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    allocate: BrokerCreateAllocate,
    db: Session = Depends(get_db),
):
    add_log(db=db, user_id=current_user.id, act="اضافه کردن تخصبص")
    create_notif(db=db, user_id=allocate.allocated_to_user_id,
                 title="rfp جدید به شما تخصیص داده شد!")
    return broker_create_allocate(db=db, allocate=allocate, creator_id=current_user.id)

#


@router.get("/allocates/", response_model=List[AllocateResponse])
async def get_allocates(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    allocate = broker_search_allocate(
        db=db, creator_id=current_user.id, skip=skip, limit=limit)
    if not allocate:
        raise HTTPException(status_code=404, detail="No allocate found")
    return allocate
#


@router.get("/single-allocate/{allocate_id}", response_model=AllocateResponse)
async def single_allocate(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    allocate_id: int,
    db: Session = Depends(get_db),
):
    allocate = broker_allocate_single(db, allocate_id=allocate_id)
    if not allocate:
        raise HTTPException(status_code=404, detail="No allocate found")
    return allocate


# # @router.get("/proposals/", response_model=List[ProposalResponse])
# # async def read_proposals(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
# #     proposals = broker_get_proposals(db, skip=skip, limit=limit)
# #     return proposals


# # Proposal-like:
# @router.get("/proposals/", response_model=List[ProposalAllResponse])
# async def read_proposals(
#     current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
#     skip: int = 0,
#     limit: int = 10,
#     info: str = None,
#     db: Session = Depends(get_db),
# ):
#     proposals = broker_get_proposals_like(
#         db, skip=skip, limit=limit, info=info)
#     return proposals


# @router.get("/proposals/{proposal_id}", response_model=ProposalSingleResponse)
# async def read_proposal(
#     current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
#     proposal_id: int,
#     db: Session = Depends(get_db),
# ):
#     proposal = broker_get_proposal_by_id(db=db, proposal_id=proposal_id)
#     # rfp = broker_get_rfp_by_id(db=db, rfp_id=proposal.RFP_id)
#     # return ProposalSingleResponse(
#     #     info=proposal.info,
#     #     comment=proposal.comment,
#     #     file_id=proposal.file_id,
#     #     RFP_info=rfp.info,
#     # )
#     return proposal


# @router.post("/commissions/")  # , response_model=ProposalResponse)
# async def add_commission(
#     current_user: Annotated[UserInfoResponse, Depends(get_current_user)],
#     commission_request: CommissionRequest,
#     db: Session = Depends(get_db),
# ):
#     proposal = broker_get_proposal_by_id(
#         db=db, proposal_id=commission_request.proposal_id
#     )

#     new_project = Project(
#         title=proposal.info,
#         proposal_id=commission_request.proposal_id,
#         user_supervisor_id=commission_request.user_supervisor_id,
#         user_discoverer_id=commission_request.user_discoverer_id,
#         user_master_id=commission_request.user_master_id,
#         user_broker_id=current_user.id,
#         user_user_id=proposal.id,
#     )
#     if commission_request.state == 1:
#         broker_create_project(db=db, new_project=new_project)
#     broker_update_proposal(
#         db=db, proposal_id=commission_request.proposal_id, state=commission_request.state)
#     return broker_create_commission(db=db, commission=commission_request)


# @router.get("/commissions/{proposal_id}", response_model=List[CommissionResponse])
# async def get_proposal_commission(
#     current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
#     proposal_id: int,
#     skip: int = 0,
#     limit: int = 10,
#     db: Session = Depends(get_db),
# ):
#     commissions = broker_get_commission(
#         db=db, proposal_id=proposal_id, skip=skip, limit=limit)

#     if not commissions:
#         raise HTTPException(status_code=404, detail="Report not found")
#     return commissions


@router.get("/users/", response_model=List[UserInfoResponse])
async def read_users_master(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    users = broker_get_users_master(db)

    return users


# @router.get("/users-discoverer/", response_model=List[UserInfoResponse])
# async def read_users_discoverer(
#     current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
#     db: Session = Depends(get_db),
# ):
#     users = broker_get_users_discoverer(db)
#     return users


# @router.get("/users-supervisor/", response_model=List[UserInfoResponse])
# async def read_users_supervisor(
#     current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
#     db: Session = Depends(get_db),
# ):
#     users = broker_get_users_supervisor(db)
#     return users
