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


def broker_create_project(db: Session, new_project: Project):
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


def broker_update_proposal(db: Session, proposal_id: int):
    updating_proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    updating_proposal.state == 1
    db.commit()
    db.refresh(updating_proposal)
