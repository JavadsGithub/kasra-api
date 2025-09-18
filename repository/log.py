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


def get_logs(
    db: Session, supervisor_id: int, skip: int = 0, limit: int = 10
):
    logs = db.query(Project).order_by(
        Project.id.desc()).offset(skip).limit(limit).all()
    return logs
