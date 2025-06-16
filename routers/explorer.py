from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model
from model.schemas import *
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from sqlalchemy import update, desc
from datetime import time

from repository.explorer import *
from util.util import *


router = APIRouter(tags=["explorer"], prefix="/explorer")


@router.get("/rfps/", response_model=List[RFPResponse])
async def read_rfps(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    rfps = explorer_get_rfps(db, skip=skip, limit=limit)
    if not rfps:
        raise HTTPException(status_code=404, detail="No RFPs found")
    return rfps


@router.get("/rfps/search/", response_model=List[RFPResponse])
async def search_rfps_endpoint(
    query: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    rfps = explorer_search_rfps(db, query=query, skip=skip, limit=limit)
    if not rfps:
        raise HTTPException(status_code=404, detail="No RFPs found matching the query")
    return rfps


@router.post("/rfps/", response_model=RFPResponse)
async def add_rfp(rfp: RFPRequest, db: Session = Depends(get_db)):
    return explorer_create_rfp(db=db, rfp=rfp)


@router.put("/rfps/{rfp_id}", response_model=RFPResponse)
async def edit_rfp(rfp_id: int, rfp_update: RFPRequest, db: Session = Depends(get_db)):
    return explorer_update_rfp(db=db, rfp_id=rfp_id, rfp_update=rfp_update)
