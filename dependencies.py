import os
from typing import Generator, Optional
from fastapi import Header, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal

ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "karthi123")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_admin(
    x_admin_token: Optional[str] = Header(None, alias="X-Admin-Token")
) -> bool:
    """Verifies that the caller has provided the correct Admin token."""
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin authorization required: missing or invalid X-Admin-Token header.",
        )
    return True
