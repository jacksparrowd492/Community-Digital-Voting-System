"""Rebuild sample_voting.db from the Alembic migrations and seed_data.sql.

Usage:
    python build_sample_db.py

sample_voting.db is a clean, committed snapshot for reviewers. The migrations
remain the authoritative schema; this script never touches voting.db.
"""
import sqlite3
import subprocess
import sys
from pathlib import Path

from seed_db import seed

BASE_DIR = Path(__file__).resolve().parent
SAMPLE_PATH = BASE_DIR / "sample_voting.db"


def main() -> int:
    SAMPLE_PATH.unlink(missing_ok=True)

    result = subprocess.run(
        [sys.executable, "-m", "alembic", "-x", f"db_url=sqlite:///{SAMPLE_PATH.as_posix()}", "upgrade", "head"],
        cwd=BASE_DIR,
    )
    if result.returncode != 0:
        print("ERROR: alembic upgrade failed.")
        return result.returncode

    if seed(SAMPLE_PATH) != 0:
        return 1

    conn = sqlite3.connect(SAMPLE_PATH)
    try:
        conn.execute("VACUUM")
        rows = conn.execute("SELECT status, COUNT(*) FROM proposals GROUP BY status ORDER BY status").fetchall()
        votes = conn.execute("SELECT COUNT(*) FROM votes").fetchone()[0]
    finally:
        conn.close()

    print(f"Built {SAMPLE_PATH.name}: proposals by status {dict(rows)}, votes {votes}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
