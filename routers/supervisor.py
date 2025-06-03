from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model, schemas
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from sqlalchemy import update, desc
from datetime import time
from repository.supervisor import *
from util.util import *


router = APIRouter(tags=["supervisor"], prefix="/supervisor")


@router.get("/proposals/", response_model=List[Proposal])
async def read_proposals(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    proposals = get_proposals(db, skip=skip, limit=limit)
    return proposals


@router.get("/proposals/", response_model=List[Proposal])
async def read_proposals(
    skip: int = 0, limit: int = 10, info: str = None, db: Session = Depends(get_db)
):
    proposals = get_proposals(db, skip=skip, limit=limit, info=info)
    return proposals


@router.get("/proposals/{proposal_id}", response_model=Proposal)
async def read_proposal(proposal_id: int, db: Session = Depends(get_db)):
    return get_proposal_by_id(db=db, proposal_id=proposal_id)
