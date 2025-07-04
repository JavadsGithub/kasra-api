from sqlalchemy.orm import Session
from model.model import *
from model.schemas import *


def suoervisor_get_projects(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Project).offset(skip).limit(limit).all()


def mentor_get_projects(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(Project)
        .filter(Project.user_master_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
