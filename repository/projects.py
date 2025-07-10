from sqlalchemy.orm import Session
from model.model import *
from model.schemas import *


def supervisor_get_projects(
    db: Session, skip: int = 0, limit: int = 10, info: str = None
):
    query = db.query(Project)
    if info:
        query = query.filter(Project.title.ilike(f"%{info}%"))
    return query.offset(skip).limit(limit).all()


def supervisor_get_single_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()


def mentor_get_projects(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(Project)
        .filter(Project.user_master_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def broker_create_project(db: Session, new_project: Project):
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project
