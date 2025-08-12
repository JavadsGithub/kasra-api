from sqlalchemy.orm import Session
from model.model import *
from model.schemas import *
from fastapi import HTTPException


def broker_get_proposals(db: Session, skip: int = 0, limit: int = 10):
    return (
        db.query(Proposal).filter(Proposal.state ==
                                  2).offset(skip).limit(limit).all()
    )


def broker_get_proposals_like(
    db: Session, skip: int = 0, limit: int = 10, info: str = None
):
    query = db.query(Proposal)
    if info:
        query = query.filter(Proposal.info.ilike(
            f"%{info}%") & Proposal.state != 1)
    return query.filter(Proposal.state != 1).offset(skip).limit(limit).all()


def explorer_get_proposals_like(
    db: Session, creator_id: int, skip: int = 0, limit: int = 10, info: str = None
):
    query = db.query(Proposal).join(RFP)
    if info:
        query = query.filter(
            Proposal.info.ilike(
                f"%{info}%") & RFP.creator_id == creator_id
        )
    return query.filter(
        RFP.creator_id == creator_id &
        Proposal.state == ProposalState.pending_to_explorer_accept,
    ).offset(skip).limit(limit).all()


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
    db: Session, user_id: int, skip: int = 0, limit: int = 10, info: str = None
):
    query = db.query(Proposal)
    if info:
        query = query.filter(Proposal.info.ilike(f"%{info}%"))
    return query.filter(Proposal.user_id == user_id).offset(skip).limit(limit).all()


def suoervisor_get_proposal_by_id(db: Session, proposal_id: int):
    proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return proposal


def explorer_update_proposal(
    db: Session, proposal_id: int, proposal_update: ExplorerUpdateProposal
):
    proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    proposal.state = ProposalState.pending_to_accept
    proposal.comment = proposal_update.comment
    proposal.supervisor_id = proposal_update.supervisor_id

    db.commit()
    db.refresh(proposal)
    return proposal


def explorer_search_proposals(creator_id: int, db: Session, skip: int = 0, limit: int = 10):
    query = db.query(Allocate).join(RFP)
    query = query.filter(RFP.creator_id == creator_id)
    return query.offset(skip).limit(limit).all()


def user_update_proposal(
    db: Session, proposal_id: int, proposal_update: UserUpdateProposal
):

    proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    if proposal_update.file_id:
        proposal.file_id = proposal_update.file_id
    db.commit()
    db.refresh(proposal)
    return proposal


def broker_update_proposal(db: Session, proposal_id: int, state: int):
    updating_proposal = db.query(Proposal).filter(
        Proposal.id == proposal_id).first()
    updating_proposal.state = state
    db.commit()
    db.refresh(updating_proposal)
