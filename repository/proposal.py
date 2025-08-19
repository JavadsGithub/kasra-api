from sqlalchemy.orm import Session
from model.model import *
from model.schemas import *
from fastapi import HTTPException


def broker_get_proposals(db: Session, skip: int = 0, limit: int = 10):
    return (
        db.query(Proposal).order_by(Proposal.id.desc()).filter(Proposal.state ==
                                                               2).offset(skip).limit(limit).all()
    )


def broker_get_proposals_like(
    db: Session, skip: int = 0, limit: int = 10, info: str = None
):
    query = db.query(Proposal).order_by(Proposal.id.desc())
    if info:
        query = query.filter(Proposal.info.ilike(
            f"%{info}%") & Proposal.state != 1)
    return query.filter(Proposal.state != 1).offset(skip).limit(limit).all()

# SUS


def explorer_get_proposals_like(
    db: Session, creator_id: int, skip: int = 0, limit: int = 10, info: str = None
):
    query = db.query(Proposal).join(RFP).order_by(Proposal.id.desc())
    if info:
        query = query.filter(
            Proposal.info.ilike(
                f"%{info}%") & RFP.creator_id == creator_id
        )
    return query.filter(

        # (Proposal.state == ProposalState.pending_to_explorer_accept) &
        (RFP.creator_id == creator_id)
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
    query = db.query(Proposal).order_by(Proposal.id.desc())
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
    proposal.commission_file_id = proposal_update.commission_file_id
    proposal.commission_date_time = proposal_update.commission_date_time

    db.commit()
    db.refresh(proposal)
    return proposal


def researcher_update_proposal_and_add_project(
    db: Session, proposal_id: int, creator_id: int
):
    proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    proposal.state = ProposalState.eccepted

    new_project = Project(
        user_supervisor_id=proposal.supervisor_id,
        user_user_id=proposal.user_id,
        state=ProjectState.active,
        creator_id=creator_id,
        created_at=datetime.now(),
        master_id=proposal.master_id,
        title=proposal.title,
        proposal_id=proposal.id,
        start_at=proposal.start_at,
        end_at=proposal.end_at,
        accepted_percent=0,
    )
    db.add(new_project)
    db.commit()
    db.refresh(proposal)
    return proposal


def researcher_update_proposal_and__not_add_project(
    db: Session, proposal_id: int, creator_id: int
):
    proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    proposal.state = ProposalState.rejected
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
    if proposal_update.start_at:
        proposal.start_at = proposal_update.start_at
    if proposal_update.end_at:
        proposal.end_at = proposal_update.end_at

    if proposal_update.applicant_name is not None:
        proposal.applicant_name = proposal_update.applicant_name
    if proposal_update.contact_number is not None:
        proposal.contact_number = proposal_update.contact_number
    if proposal_update.education is not None:
        proposal.education = proposal_update.education
    if proposal_update.expertise is not None:
        proposal.expertise = proposal_update.expertise
    if proposal_update.project_duration is not None:
        proposal.project_duration = proposal_update.project_duration
    if proposal_update.project_goals is not None:
        proposal.project_goals = proposal_update.project_goals
    if proposal_update.project_importance is not None:
        proposal.project_importance = proposal_update.project_importance
    if proposal_update.technical_details is not None:
        proposal.technical_details = proposal_update.technical_details
    if proposal_update.product_features is not None:
        proposal.product_features = proposal_update.product_features
    if proposal_update.similar_products is not None:
        proposal.similar_products = proposal_update.similar_products
    if proposal_update.project_outcomes is not None:
        proposal.project_outcomes = proposal_update.project_outcomes
    if proposal_update.project_innovation is not None:
        proposal.project_innovation = proposal_update.project_innovation
    if proposal_update.project_risks is not None:
        proposal.project_risks = proposal_update.project_risks

    proposal.state = ProposalState.pending_to_explorer_accept
    db.commit()
    db.refresh(proposal)
    return proposal


def broker_update_proposal(db: Session, proposal_id: int, state: int):
    updating_proposal = db.query(Proposal).filter(
        Proposal.id == proposal_id).first()
    updating_proposal.state = state
    db.commit()
    db.refresh(updating_proposal)


def researcher_get_proposals_like(
    db: Session, creator_id: int, skip: int = 0, limit: int = 10, info: str = None
):
    query = db.query(Proposal).join(RFP).order_by(Proposal.id.desc())
    if info:
        query = query.filter(
            Proposal.info.ilike(
                f"%{info}%")
        )
    return query.offset(skip).limit(limit).all()


def researcher_get_proposal_by_id(db: Session, proposal_id: int):
    proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return proposal
