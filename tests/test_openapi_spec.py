import json
from pathlib import Path

from main import app

SPEC_PATH = Path(__file__).resolve().parent.parent / "openapi.json"


def test_committed_openapi_spec_matches_app():
    """openapi.json (the SDK generator input) must match the live API.

    If this fails, re-export the spec and regenerate the SDK (see README, "Python SDK").
    """
    committed = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    assert committed == app.openapi(), (
        "openapi.json is stale: re-export it and regenerate voting_sdk/"
    )
