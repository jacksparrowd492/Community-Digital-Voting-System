from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import schemas
from dependencies import get_db
import services.votes as vote_service

router = APIRouter(prefix="/votes", tags=["votes"])


@router.delete(
    "/{vote_id}",
    response_model=schemas.MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Revoke a vote",
)
def revoke_vote(
    vote_id: int,
    db: Session = Depends(get_db),
):
    """Revoke a previously cast vote, permitted only while the proposal remains active."""
    return vote_service.revoke_vote(db, vote_id)
