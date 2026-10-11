from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import schemas
from dependencies import get_db, require_admin
import services.proposals as proposal_service
import services.votes as vote_service

router = APIRouter(prefix="/proposals", tags=["proposals"])


@router.post(
    "/",
    response_model=schemas.ProposalResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new proposal",
)
def create_proposal(
    proposal_in: schemas.ProposalCreate,
    db: Session = Depends(get_db),
):
    """Create a new proposal for voting."""
    return proposal_service.create_proposal(db, proposal_in)


@router.get(
    "/",
    response_model=List[schemas.ProposalResponse],
    summary="Retrieve all proposals",
)
def list_proposals(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Retrieve all proposals, optionally filtered by status ('active', 'closed', 'expired')."""
    return proposal_service.get_all_proposals(db, status=status)


@router.get(
    "/{proposal_id}",
    response_model=schemas.ProposalDetailResponse,
    summary="View a specific proposal with current vote counts",
)
def get_proposal(
    proposal_id: int,
    db: Session = Depends(get_db),
):
    """View details of a specific proposal along with current vote counts."""
    proposal = proposal_service.get_proposal_by_id(db, proposal_id)
    if not proposal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proposal with ID {proposal_id} not found",
        )
    vote_counts = proposal_service.get_proposal_vote_counts(db, proposal_id)
    return schemas.ProposalDetailResponse(
        id=proposal.id,
        title=proposal.title,
        description=proposal.description,
        created_at=proposal.created_at,
        deadline=proposal.deadline,
        status=proposal.status,
        vote_counts=vote_counts,
    )


@router.patch(
    "/{proposal_id}/close",
    response_model=schemas.ProposalResponse,
    summary="Manually close a proposal (Admin)",
)
def close_proposal(
    proposal_id: int,
    db: Session = Depends(get_db),
    _admin: bool = Depends(require_admin),
):
    """Manually close an active proposal."""
    proposal = proposal_service.get_proposal_by_id(db, proposal_id)
    if not proposal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proposal with ID {proposal_id} not found",
        )
    if proposal.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot close a proposal that is already '{proposal.status}'",
        )
    return proposal_service.close_proposal(db, proposal)


@router.post(
    "/{proposal_id}/vote",
    response_model=schemas.VoteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a vote for a proposal",
)
def vote_on_proposal(
    proposal_id: int,
    vote_in: schemas.VoteCreate,
    db: Session = Depends(get_db),
):
    """Submit a vote ('yes', 'no', or 'abstain') on an active proposal."""
    return vote_service.cast_vote(db, proposal_id, vote_in)
