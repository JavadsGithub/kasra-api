from fastapi import HTTPException
from sqlalchemy.orm import Session
from model.model import *
from model.schemas import *
from repository.user import create_notif


def add_log(db: Session, user_id: int, act: str):
    user = db.query(User).filter(User.id == user_id).first()
    user_name = user.fname+" "+user.lname
    new_log = Log(
        user_name=user_name,
        act=act,
        created_at=datetime.now(),)

    db.add(new_log)
    db.commit()
    db.refresh(new_log)


def get_logs(
    db: Session, skip: int = 0, limit: int = 10
):
    logs = db.query(Log).order_by(
        Log.id.desc()).offset(skip).limit(limit).all()
    return logs
