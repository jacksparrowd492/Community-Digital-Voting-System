from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

import models
import schemas
from services.proposals import check_and_update_status


def cast_vote(
    db: Session, proposal_id: int, vote_in: schemas.VoteCreate
) -> models.Vote:
    proposal = db.get(models.Proposal, proposal_id)
    if not proposal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proposal with ID {proposal_id} not found",
        )

    proposal = check_and_update_status(db, proposal)
    if proposal.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot vote on proposal with status '{proposal.status}'",
        )

    # Check for existing vote by this voter
    existing_vote = db.execute(
        select(models.Vote).where(
            models.Vote.proposal_id == proposal_id,
            models.Vote.voter_name == vote_in.voter_name,
        )
    ).scalar_one_or_none()

    if existing_vote:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Voter '{vote_in.voter_name}' has already voted on proposal {proposal_id}",
        )

    new_vote = models.Vote(
        proposal_id=proposal_id,
        voter_name=vote_in.voter_name,
        vote=vote_in.vote,
    )
    db.add(new_vote)
    try:
        db.commit()
        db.refresh(new_vote)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Voter '{vote_in.voter_name}' has already voted on proposal {proposal_id}",
        )
    return new_vote


def revoke_vote(db: Session, vote_id: int) -> dict:
    vote = db.get(models.Vote, vote_id)
    if not vote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vote with ID {vote_id} not found",
        )

    proposal = db.get(models.Proposal, vote.proposal_id)
    if proposal:
        proposal = check_and_update_status(db, proposal)
        if proposal.status != "active":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot revoke vote because proposal is '{proposal.status}'",
            )

    db.delete(vote)
    db.commit()
    return {"message": f"Vote {vote_id} revoked successfully"}
