from datetime import datetime, timedelta
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base
import models
from dependencies import ADMIN_TOKEN, get_db
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


def _create_proposal(title="Test Proposal"):
    res = client.post(
        "/proposals/",
        json={"title": title, "description": "Created by a test."},
    )
    assert res.status_code == 201
    return res.json()["id"]


def _move_deadline_into_past(proposal_id):
    """Simulate the deadline passing on a proposal that was created active."""
    db = TestingSessionLocal()
    try:
        proposal = db.get(models.Proposal, proposal_id)
        proposal.deadline = datetime.utcnow() - timedelta(minutes=1)
        db.commit()
    finally:
        db.close()


def test_reject_vote_after_deadline_passes():
    prop_id = _create_proposal("Bike Lanes")

    # Voting works while the proposal is active
    ok = client.post(
        f"/proposals/{prop_id}/vote",
        json={"voter_name": "Frank", "vote": "yes"},
    )
    assert ok.status_code == 201

    _move_deadline_into_past(prop_id)

    late = client.post(
        f"/proposals/{prop_id}/vote",
        json={"voter_name": "Grace", "vote": "no"},
    )
    assert late.status_code == 400
    assert "expired" in late.json()["detail"]

    # The earlier vote is still counted and no new vote was added
    detail = client.get(f"/proposals/{prop_id}").json()
    assert detail["status"] == "expired"
    assert detail["vote_counts"]["total"] == 1


def test_reject_revocation_after_expiration():
    prop_id = _create_proposal("Dog Park")
    vote_id = client.post(
        f"/proposals/{prop_id}/vote",
        json={"voter_name": "Heidi", "vote": "yes"},
    ).json()["id"]

    _move_deadline_into_past(prop_id)

    revoke = client.delete(f"/votes/{vote_id}")
    assert revoke.status_code == 400
    assert "expired" in revoke.json()["detail"]

    # Vote must remain in the tally
    detail = client.get(f"/proposals/{prop_id}").json()
    assert detail["vote_counts"]["yes"] == 1


@pytest.mark.parametrize(
    "headers",
    [{}, {"X-Admin-Token": "wrong-token"}, {"X-Admin-Token": ""}],
    ids=["missing", "invalid", "empty"],
)
def test_reject_close_without_valid_admin_token(headers):
    prop_id = _create_proposal("Town Hall Wi-Fi")

    res = client.patch(f"/proposals/{prop_id}/close", headers=headers)
    assert res.status_code == 401

    # Proposal must stay open
    assert client.get(f"/proposals/{prop_id}").json()["status"] == "active"


def test_admin_can_close_active_proposal():
    prop_id = _create_proposal("Farmers Market")

    res = client.patch(
        f"/proposals/{prop_id}/close", headers={"X-Admin-Token": ADMIN_TOKEN}
    )
    assert res.status_code == 200
    assert res.json()["status"] == "closed"
    assert client.get(f"/proposals/{prop_id}").json()["status"] == "closed"

    # Closing an already-closed proposal is rejected
    again = client.patch(
        f"/proposals/{prop_id}/close", headers={"X-Admin-Token": ADMIN_TOKEN}
    )
    assert again.status_code == 400


def test_not_found_errors():
    missing = 99999
    admin = {"X-Admin-Token": ADMIN_TOKEN}

    assert client.get(f"/proposals/{missing}").status_code == 404
    assert client.patch(f"/proposals/{missing}/close", headers=admin).status_code == 404
    assert (
        client.post(
            f"/proposals/{missing}/vote",
            json={"voter_name": "Ivan", "vote": "yes"},
        ).status_code
        == 404
    )

    res = client.delete(f"/votes/{missing}")
    assert res.status_code == 404
    assert "not found" in res.json()["detail"]


def test_reject_invalid_vote_payload():
    prop_id = _create_proposal("Playground Upgrade")

    bad_choice = client.post(
        f"/proposals/{prop_id}/vote",
        json={"voter_name": "Judy", "vote": "maybe"},
    )
    assert bad_choice.status_code == 422

    empty_name = client.post(
        f"/proposals/{prop_id}/vote",
        json={"voter_name": "", "vote": "yes"},
    )
    assert empty_name.status_code == 422
