from sqlalchemy.orm import Session
from model.model import *
from model.schemas import *
from fastapi import HTTPException


def broker_get_proposals(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Proposal).offset(skip).limit(limit).all()


def broker_get_proposals_like(
    db: Session, skip: int = 0, limit: int = 10, info: str = None
):
    query = db.query(Proposal)

    if info:
        query = query.filter(Proposal.info.ilike(f"%{info}%"))
    return query.offset(skip).limit(limit).all()


def broker_get_proposal_by_id(db: Session, proposal_id: int):
    proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return proposal


def suoervisor_get_proposals(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Proposal).offset(skip).limit(limit).all()


def suoervisor_get_proposals_like(
    db: Session, skip: int = 0, limit: int = 10, info: str = None
):
    query = db.query(Proposal)

    if info:
        query = query.filter(Proposal.info.ilike(f"%{info}%"))
    return query.offset(skip).limit(limit).all()


def suoervisor_get_proposal_by_id(db: Session, proposal_id: int):
    proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return proposal


def suoervisor_update_proposal(
    db: Session, proposal_id: int, proposal_update: ProposalUpdate
):
    proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    proposal.state = proposal_update.state
    proposal.comment = proposal_update.comment

    db.commit()
    db.refresh(proposal)
    return proposal
