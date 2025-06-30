from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from datetime import time
import datetime
from service.user import reports_exist
from repository.user import *
from util.util import *
from util import util

router = APIRouter(tags=["seed"], prefix="/seed")


@router.get("/seed/")
async def add_proposal(db: Session = Depends(get_db)):
    db = database.SessionLocal()

    new_user_roules = [
        UserRole(title="کارگزار"),
        UserRole(title="کاشف"),
        UserRole(title="کاربر"),
        UserRole(title="ناظر"),
        UserRole(title="استاد راهنما"),
    ]
    db.add_all(new_user_roules)
    db.commit()
    new_file = File(info="file.pdf", access_id=1)
    db.add(new_file)
    db.commit()

    rolese = db.query(UserRole).all()
    my_file = db.query(File).first()
    file_i = my_file.id
    new_users = [
        User(
            user_type_id=rolese[0].id,
            fname="جواد",
            lname="جوادی",
            father_name="محمدجواد",
            resume_file_id=file_i,
            birth=datetime.now(),
            address="همدان-جوادیه",
            username="admin",
            password=util.hash("admin"),
            phone="09181020300",
            active=True,
        ),
        User(
            user_type_id=rolese[1].id,
            fname="علی",
            lname="اکبری",
            father_name="حسن",
            birth=datetime.now(),
            resume_file_id=file_i,
            address="تهران-اکبرآباد",
            username="admin2",
            password=util.hash("admin"),
            phone="09182020301",
            active=True,
        ),
        User(
            user_type_id=rolese[2].id,
            fname="سارا",
            lname="موسوی",
            father_name="محمد",
            birth=datetime.now(),
            resume_file_id=file_i,
            address="اصفهان-موسوی",
            username="admin3",
            password=util.hash("admin"),
            phone="09183020302",
            active=True,
        ),
        User(
            user_type_id=rolese[3].id,
            fname="زهرا",
            lname="حسینی",
            father_name="علی",
            birth=datetime.now(),
            resume_file_id=file_i,
            address="شیراز-حسینیه",
            username="admin4",
            password=util.hash("admin"),
            phone="09184020303",
            active=True,
        ),
        User(
            user_type_id=rolese[4].id,
            fname="رضا",
            lname="نیکو",
            father_name="سید",
            birth=datetime.now(),
            resume_file_id=file_i,
            address="مشهد-رضوی",
            username="admin5",
            password=util.hash("admin"),
            phone="09185020304",
            active=True,
        ),
    ]
    new_RFP_fields = [
        RFPField(title="صنعت خودرو"),
        RFPField(title="کامپیوتر و it"),
        RFPField(title="کشاورزی"),
        RFPField(title="صنایع شیمی"),
        RFPField(title="صنایع هوافضا"),
        RFPField(title="امنیت سایبری"),
        RFPField(title="هوش مصنوعی"),
        RFPField(title="صنایع دفاعی"),
        RFPField(title="علوم انسانی"),
    ]
    db.add_all(new_RFP_fields)
    db.commit()
    db.add_all(new_users)
    db.commit()

    return {"response": "ok"}
