from datetime import datetime
from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Proposal(Base):
    __tablename__ = "proposals"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    deadline: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(
        String(10), default="active", nullable=False
    )

    votes: Mapped[list["Vote"]] = relationship(
        "Vote", back_populates="proposal", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('active', 'closed', 'expired')",
            name="check_proposal_status",
        ),
    )


class Vote(Base):
    __tablename__ = "votes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    proposal_id: Mapped[int] = mapped_column(
        ForeignKey("proposals.id", ondelete="CASCADE"), nullable=False
    )
    voter_name: Mapped[str] = mapped_column(String(100), nullable=False)
    vote: Mapped[str] = mapped_column(String(10), nullable=False)
    voted_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    proposal: Mapped["Proposal"] = relationship(
        "Proposal", back_populates="votes"
    )

    __table_args__ = (
        CheckConstraint(
            "vote IN ('yes', 'no', 'abstain')",
            name="check_vote_value",
        ),
        UniqueConstraint(
            "proposal_id", "voter_name",
            name="unique_voter_proposal",
        ),
    )
