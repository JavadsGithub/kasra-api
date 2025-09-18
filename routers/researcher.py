from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model, schemas
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from sqlalchemy import update, desc
from datetime import time

from repository.allocate import broker_allocate_single, broker_search_allocate, explorer_allocate_single, explorer_update_allocate, researcher_accept_allocate, researcher_reject_allocate, researcher_search_allocate
from repository.projects import *
from repository.proposal import researcher_get_proposals_like, researcher_update_proposal_and__not_add_project, researcher_update_proposal_and_add_project, supervisor_update_proposal
from repository.reports import *
from model.schemas import *
from repository.user import create_notif, researcher_get_masters_like
from util.util import *
from service.mentor import *

router = APIRouter(tags=["researcher"], prefix="/researcher")

#


@router.get("/projects/", response_model=List[ProjectResponse])
async def get_project(
    current_user: Annotated[UserInfoResponse, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    user_id = current_user.id
    projects = researcher_get_projects(
        db=db, user_id=user_id, skip=skip, limit=limit)
    return projects

#


@router.get("/reports/{project_id}")
async def get_reports(
    current_user: Annotated[UserInfoResponse, Depends(get_current_user)],
    project_id: int = 0,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):

    return researcher_get_report(db=db, project_id=project_id, skip=skip, limit=limit)

#


@router.get("/single-report/{report_id}")
async def get_single_reports(
    current_user: Annotated[UserInfoResponse, Depends(get_current_user)],
    report_id: int = 0,
    db: Session = Depends(get_db),
):
    return researcher_get_one_report(db=db, report_id=report_id,)

#


@router.get("/all-reports/")
async def get_all_reports(
    current_user: Annotated[UserInfoResponse, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):

    return researcher_get_all_report(db=db, skip=skip, limit=limit)
# OLD ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^6

#


@router.put("/allocates/{allocate_id}", response_model=AllocateResponse)
async def edit_allocate(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    allocate_id: int,
    accept: bool = False,
    db: Session = Depends(get_db),
):
    if accept:

        return researcher_accept_allocate(db=db, allocate_id=allocate_id)
    else:
        return researcher_reject_allocate(db=db, allocate_id=allocate_id)

#


@router.put("/master-allocates/{allocate_id}", response_model=AllocateResponse)
async def edit_master_allocate(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    allocate_id: int,
    allocate_update: ExplorerUpdateAllocate,
    db: Session = Depends(get_db),
):
    allocate = explorer_allocate_single(db, allocate_id=allocate_id)
    if not allocate:
        raise HTTPException(status_code=404, detail="No allocate found")
    new_proposal = model.Proposal(
        creator_id=current_user.id,
        created_at=datetime.now(),
        master=allocate.master,
        title=allocate.project_title,
        description=allocate.project_description,
        RFP_id=allocate.RFP_id,
        allocate_id=allocate_id,

        # supervisor_id=Column(Integer, ForeignKey("user.id"), nullable=True),
        user_id=allocate.allocated_to_user_id,
        state=model.ProposalState.pending_to_fill,  # ENUM
        comment=""
    )
    db.add(new_proposal)
    db.commit()
    create_notif(db=db, user_id=allocate.allocated_to_user_id,
                 title="وضعیت پروپوزال تغییر کرد")
    return explorer_update_allocate(db=db, allocate_update=allocate_update, allocate_id=allocate_id)


@router.get("/allocates/", response_model=List[AllocateResponse])
async def get_allocates(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    allocate = researcher_search_allocate(
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
    allocate = broker_allocate_single(db=db, allocate_id=allocate_id)
    if not allocate:
        raise HTTPException(status_code=404, detail="No allocate found")
    return allocate

#


@router.put("/projects/{project_id}", response_model=ProjectResponse)
async def edit_accepting_project(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    project_id: int,
    project_update: ResearcherProjectUpdate,
    db: Session = Depends(get_db),
):
    return researcher_accept_project(db=db, project_id=project_id, project_update=project_update)

# edit


@router.put("/proposal/{proposal_id}", response_model=ProposalResponse)
async def edit_proposal_and_create_project(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    proposal_id: int,
    # proposal_update: ResearcherUpdateProposal,
    accept: bool,
    db: Session = Depends(get_db),
):
    if accept:
        return researcher_update_proposal_and_add_project(
            db=db, proposal_id=proposal_id,  creator_id=current_user.id
        )
    else:
        return researcher_update_proposal_and__not_add_project(
            db=db, proposal_id=proposal_id, creator_id=current_user.id
        )


@router.get("/proposals/", response_model=List[ProposalResponse])
async def read_proposals(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 10,
    info: str = None,
    db: Session = Depends(get_db),
):
    proposals = researcher_get_proposals_like(
        db=db, skip=skip, limit=limit, info=info, creator_id=current_user.id)
    return proposals


@router.post("/add-master/", response_model=MasterResponse)
async def read_proposals(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    new_master: MasterRequest,

    db: Session = Depends(get_db),
):
    new_db_master = Master(
        name=new_master.name
    )
    db.add(new_db_master)
    db.commit()
    db.refresh(new_db_master)
    return new_db_master


@router.get("/masters/", response_model=List[MasterResponse])
async def read_masters(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    name: str = None,
):

    users = researcher_get_masters_like(
        db=db, skip=skip, limit=limit, name=name)
    return users


@router.put("/update-master/{master_id}", response_model=MasterResponse)
async def update_master(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    update_master: MasterRequest,
    master_id: int,
    db: Session = Depends(get_db),
):
    master = db.query(Master).filter(Master.id == master_id).first()
    if not master:
        raise HTTPException(
            status_code=403, detail="master dose not exists"
        )
    if update_master.name:
        master.name = update_master.name

    db.commit()
    db.refresh(master)
    return master


@router.put("/accept-proposal/{proposal_id}", response_model=ProposalResponse)
async def edit_proposal(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    proposal_id: int,
    proposal_update: SupervisorUpdateProposal,
    db: Session = Depends(get_db),

):
    return supervisor_update_proposal(
        db=db, proposal_id=proposal_id, proposal_update=proposal_update
    )


@router.put("/user/{user_id}", response_model=UserInfoResponse)
async def change_password(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    user_id: int,
    new_password: str,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    user.password = hash(password=new_password)

    db.commit()
    db.refresh(user)
    return user


# @router.delete("/delete-master/{master_id}", response_model=MasterResponse)
# async def update_master(
#     current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
#     master_id: int,
#     db: Session = Depends(get_db),
# ):
#     master = db.query(Master).filter(Master.id == master_id).first()
#     if not master:
#         raise HTTPException(
#             status_code=403, detail="master dose not exists"
#         )
#     db.delete(master)
#     db.commit()
#     return master
