from sqlalchemy.orm import Session
from model.model import *
from model.schemas import *
from fastapi import HTTPException


def broker_get_proposals(db: Session, skip: int = 0, limit: int = 10):
    return (
        db.query(Proposal).filter(Proposal.state == 2).offset(skip).limit(limit).all()
    )


def broker_get_proposals_like(
    db: Session, skip: int = 0, limit: int = 10, info: str = None
):
    query = db.query(Proposal)
    if info:
        query = query.filter(Proposal.info.ilike(f"%{info}%")& Proposal.state != 1)
    return query.filter(Proposal.state != 1).offset(skip).limit(limit).all()


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


def user_get_proposals_like(
    db: Session, skip: int = 0, limit: int = 10, info: str = None
):
    query = db.query(Proposal)

    if info:
        query = query.filter(Proposal.info.ilike(f"%{info}%"))
    return query.offset(skip).limit(limit).all()


def user_get_proposals_like(
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


def user_update_proposal(
    db: Session, proposal_id: int, proposal_update: ProposalUserUpdateRequest
):

    proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    if proposal_update.info:
        proposal.info = proposal_update.info
    if proposal_update.RFP_id:
        proposal.RFP_id = proposal_update.RFP_id
    if proposal_update.file_id:
        proposal.file_id = proposal_update.file_id
    db.commit()
    db.refresh(proposal)
    return proposal


def broker_update_proposal(db: Session, proposal_id: int):
    updating_proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    updating_proposal.state == 1
    db.commit()
    db.refresh(updating_proposal)
