from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, Field


# --- Proposal Schemas ---

class ProposalBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Title of the proposal")
    description: str = Field(..., min_length=1, description="Detailed proposal description")


class ProposalCreate(ProposalBase):
    deadline: Optional[datetime] = Field(
        None,
        description="Voting deadline in UTC. Defaults to 2 days from now if not specified.",
    )


class ProposalResponse(ProposalBase):
    id: int
    created_at: datetime
    deadline: datetime
    status: Literal["active", "closed", "expired"]

    model_config = ConfigDict(from_attributes=True)


class VoteCounts(BaseModel):
    yes: int = 0
    no: int = 0
    abstain: int = 0
    total: int = 0


class ProposalDetailResponse(ProposalResponse):
    vote_counts: VoteCounts


# --- Vote Schemas ---

class VoteCreate(BaseModel):
    voter_name: str = Field(..., min_length=1, max_length=100, description="Name or identifier of the voter")
    vote: Literal["yes", "no", "abstain"] = Field(..., description="Vote choice ('yes', 'no', 'abstain')")


class VoteResponse(BaseModel):
    id: int
    proposal_id: int
    voter_name: str
    vote: Literal["yes", "no", "abstain"]
    voted_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    message: str
