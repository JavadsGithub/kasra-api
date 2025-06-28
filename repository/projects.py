from sqlalchemy.orm import Session
from model.model import *
from model.schemas import *


def suoervisor_get_projects(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Project).offset(skip).limit(limit).all()
