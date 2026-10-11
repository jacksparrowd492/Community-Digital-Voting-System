from datetime import datetime, timedelta
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base
from dependencies import get_db
from main import app

# In-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    bind=test_engine, autoflush=False, autocommit=False
)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_and_get_proposal():
    response = client.post(
        "/proposals/",
        json={
            "title": "Park Renovation",
            "description": "Plant trees and install benches in community park.",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Park Renovation"
    assert data["status"] == "active"
    proposal_id = data["id"]

    # Retrieve proposal with counts
    detail_res = client.get(f"/proposals/{proposal_id}")
    assert detail_res.status_code == 200
    detail = detail_res.json()
    assert detail["vote_counts"]["total"] == 0
    assert detail["vote_counts"]["yes"] == 0


def test_voting_flow_and_uniqueness():
    # Create proposal
    prop_res = client.post(
        "/proposals/",
        json={"title": "Solar Panels", "description": "Community solar project."},
    )
    prop_id = prop_res.json()["id"]

    # User 1 votes Yes
    vote1 = client.post(
        f"/proposals/{prop_id}/vote",
        json={"voter_name": "Alice", "vote": "yes"},
    )
    assert vote1.status_code == 201
    vote1_id = vote1.json()["id"]

    # User 1 votes again on same proposal -> reject (400)
    dup_vote = client.post(
        f"/proposals/{prop_id}/vote",
        json={"voter_name": "Alice", "vote": "no"},
    )
    assert dup_vote.status_code == 400

    # User 2 votes No
    vote2 = client.post(
        f"/proposals/{prop_id}/vote",
        json={"voter_name": "Bob", "vote": "no"},
    )
    assert vote2.status_code == 201

    # Check vote counts
    detail = client.get(f"/proposals/{prop_id}").json()
    assert detail["vote_counts"]["yes"] == 1
    assert detail["vote_counts"]["no"] == 1
    assert detail["vote_counts"]["total"] == 2

    # User 1 revokes vote
    revoke_res = client.delete(f"/votes/{vote1_id}")
    assert revoke_res.status_code == 200

    # Vote count decreases
    detail_after = client.get(f"/proposals/{prop_id}").json()
    assert detail_after["vote_counts"]["yes"] == 0
    assert detail_after["vote_counts"]["total"] == 1

    # User 1 can now vote again
    revote = client.post(
        f"/proposals/{prop_id}/vote",
        json={"voter_name": "Alice", "vote": "abstain"},
    )
    assert revote.status_code == 201


def test_cannot_vote_or_revoke_on_closed_proposal():
    prop_res = client.post(
        "/proposals/",
        json={"title": "Library Hours", "description": "Extend evening hours."},
    )
    prop_id = prop_res.json()["id"]

    # Vote first
    vote_res = client.post(
        f"/proposals/{prop_id}/vote",
        json={"voter_name": "Charlie", "vote": "yes"},
    )
    vote_id = vote_res.json()["id"]

    # Close proposal without admin token -> 401 Unauthorized
    unauth_close = client.patch(f"/proposals/{prop_id}/close")
    assert unauth_close.status_code == 401

    # Close proposal with valid admin token -> 200 OK
    close_res = client.patch(
        f"/proposals/{prop_id}/close", headers={"X-Admin-Token": "karthi123"}
    )
    assert close_res.status_code == 200
    assert close_res.json()["status"] == "closed"

    # New vote should be rejected
    rejected_vote = client.post(
        f"/proposals/{prop_id}/vote",
        json={"voter_name": "Dave", "vote": "no"},
    )
    assert rejected_vote.status_code == 400

    # Revoking existing vote should be rejected
    rejected_revoke = client.delete(f"/votes/{vote_id}")
    assert rejected_revoke.status_code == 400


def test_proposal_auto_expiration():
    # Create proposal with deadline in the past
    past_deadline = (datetime.utcnow() - timedelta(minutes=5)).isoformat()
    prop_res = client.post(
        "/proposals/",
        json={
            "title": "Expired Proposal",
            "description": "Deadline already passed.",
            "deadline": past_deadline,
        },
    )
    prop_id = prop_res.json()["id"]

    # Fetching should auto-expire
    detail = client.get(f"/proposals/{prop_id}").json()
    assert detail["status"] == "expired"

    # Voting must be rejected
    vote_res = client.post(
        f"/proposals/{prop_id}/vote",
        json={"voter_name": "Eve", "vote": "yes"},
    )
    assert vote_res.status_code == 400
