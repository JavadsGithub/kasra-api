from fastapi import HTTPException
from sqlalchemy.orm import Session
from model.model import *
from model.schemas import *
from repository.user import create_notif


def add_log(db: Session, user_id: int, act: str):
    user = db.query(User).filter(User.id == user_id).first()
    log = Log(
        user_name=user.fname+user.lname,
        act=act,
        created_at=datetime.now(),)

    db.add(log)
    db.commit()
