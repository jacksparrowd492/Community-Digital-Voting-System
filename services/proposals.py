from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, func

import models
import schemas


def check_and_update_status(db: Session, proposal: models.Proposal) -> models.Proposal:
    """Auto-expires an active proposal if its deadline has passed."""
    if proposal.status == "active" and datetime.utcnow() >= proposal.deadline:
        proposal.status = "expired"
        db.commit()
        db.refresh(proposal)
    return proposal


def create_proposal(db: Session, data: schemas.ProposalCreate) -> models.Proposal:
    deadline = data.deadline or (datetime.utcnow() + timedelta(days=2))
    proposal = models.Proposal(
        title=data.title,
        description=data.description,
        deadline=deadline,
        status="active",
    )
    db.add(proposal)
    db.commit()
    db.refresh(proposal)
    return proposal


def get_all_proposals(
    db: Session, status: Optional[str] = None
) -> List[models.Proposal]:
    proposals = db.execute(select(models.Proposal)).scalars().all()
    # Check and update status for all
    updated_proposals = []
    for p in proposals:
        updated_p = check_and_update_status(db, p)
        if status is None or updated_p.status == status:
            updated_proposals.append(updated_p)
    return updated_proposals


def get_proposal_by_id(db: Session, proposal_id: int) -> Optional[models.Proposal]:
    proposal = db.get(models.Proposal, proposal_id)
    if proposal:
        return check_and_update_status(db, proposal)
    return None


def get_proposal_vote_counts(db: Session, proposal_id: int) -> schemas.VoteCounts:
    counts_query = (
        db.query(models.Vote.vote, func.count(models.Vote.id))
        .filter(models.Vote.proposal_id == proposal_id)
        .group_by(models.Vote.vote)
        .all()
    )
    counts_dict = dict(counts_query)
    yes_count = counts_dict.get("yes", 0)
    no_count = counts_dict.get("no", 0)
    abstain_count = counts_dict.get("abstain", 0)
    total_count = yes_count + no_count + abstain_count

    return schemas.VoteCounts(
        yes=yes_count,
        no=no_count,
        abstain=abstain_count,
        total=total_count,
    )


def close_proposal(db: Session, proposal: models.Proposal) -> models.Proposal:
    proposal.status = "closed"
    db.commit()
    db.refresh(proposal)
    return proposal
