from fastapi import HTTPException
from sqlalchemy.orm import Session
from model.model import *
from model.schemas import *
from repository.user import create_notif


def supervisor_get_projects(
    db: Session, supervisor_id: int, skip: int = 0, limit: int = 10, info: str = None
):
    query = db.query(Project).order_by(Project.id.desc())
    if info:
        query = query.filter(Project.title.ilike(f"%{info}%"))
    return query.filter((Project.user_supervisor_id == supervisor_id)).offset(skip).limit(limit).all()


def supervisor_get_single_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()

# sus


def researcher_get_projects(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(Project).order_by(Project.id.desc())
        # .filter((Project.accepted_percent >= 100) & (Project.state == ProjectState.active))
        .offset(skip)
        .limit(limit)
        .all()
    )


def broker_create_project(db: Session, new_project: Project):
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


def researcher_accept_project(
    db: Session, project_id: int, project_update: ResearcherProjectUpdate
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="project not found")
    if project_update.commission_file_id:
        project.commission_file_id = project_update.commission_file_id

    project.state = ProjectState.ended

    db.commit()
    db.refresh(project)
    create_notif(db=db, user_id=project.user_user_id,
                 title="وضعیت پروژه تغییر کرد")
    return project
