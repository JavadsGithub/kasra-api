from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
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


# @router.get("/seed/")
# async def add_proposal(db: Session = Depends(get_db)):
#     new_RFP_fields = [
#         model.RFPField(title="صنعت خودرو"),
#         model.RFPField(title="کامپیوتر و it"),
#         model.RFPField(title="کشاورزی"),
#         model.RFPField(title="صنایع شیمی"),
#         model.RFPField(title="صنایع هوافضا"),
#         model.RFPField(title="امنیت سایبری"),
#         model.RFPField(title="هوش مصنوعی"),
#         model.RFPField(title="صنایع دفاعی"),
#         model.RFPField(title="علوم انسانی"),
#     ]
#     db.add_all(new_RFP_fields)
#     db.commit()
#     return {"response": "ok"}


# @router.get("/rfps/", response_model=List[RFPResponse])
# async def read_rfps(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     rfps = explorer_get_rfps(db, skip=skip, limit=limit)
#     rfps_exist(rfps)
#     return rfps


@router.get("/rfp-fields/", response_model=List[RFPFieldResponse])
async def read_rfp_fields(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    rfp_fields = explorer_get_rfp_fields(db, skip=skip, limit=limit)
    rfps_exist(rfp_fields)
    return rfp_fields


@router.get("/rfps/", response_model=List[RFPResponse])
async def search_rfps_endpoint(
    query: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    rfps = explorer_search_rfps(db, query=query, skip=skip, limit=limit)
    rfps_exist(rfps)
    return rfps


@router.post("/rfps/", response_model=RFPResponse)
async def add_rfp(rfp: RFPRequest, db: Session = Depends(get_db)):
    return explorer_create_rfp(db=db, rfp=rfp)


@router.put("/rfps/{rfp_id}", response_model=RFPResponse)
async def edit_rfp(rfp_id: int, rfp_update: RFPRequest, db: Session = Depends(get_db)):
    return explorer_update_rfp(db=db, rfp_id=rfp_id, rfp_update=rfp_update)
