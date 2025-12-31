import sqlite3
import shutil
import sys
from pathlib import Path


def _data_dir() -> Path:
    """Return a writable data directory.

    - When bundled (sys.frozen), use a folder in the user's home (e.g. ~/.expense_tracker).
    - Otherwise use the project's `data` directory so local development keeps using it.
    If an existing DB is found in the project `data/expenses.db` and we are using the user data dir,
    migrate it by copying.
    """
    if getattr(sys, "frozen", False):
        base = Path.home() / ".expense_tracker"
    else:
        base = Path(__file__).parent.parent / "data"
    base.mkdir(parents=True, exist_ok=True)

    # Migrate project DB to user data dir if needed (only for frozen mode)
    project_db = Path(__file__).parent.parent / "data" / "expenses.db"
    user_db = base / "expenses.db"
    try:
        if getattr(sys, "frozen", False) and project_db.exists() and not user_db.exists():
            shutil.copy2(project_db, user_db)
    except Exception:
        # Best-effort migration; ignore errors
        pass

    return base


DB_PATH = _data_dir() / "expenses.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            note TEXT
        )
    """)

    conn.commit()
    conn.close()
