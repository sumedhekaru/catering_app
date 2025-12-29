"""Utility script to create the SQLite database for the catering app."""
from __future__ import annotations

import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "app" / "caterers.db"
SCHEMA_PATH = BASE_DIR / "create_tables.sql"


def main() -> None:
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(
            f"Schema file not found: {SCHEMA_PATH}. Ensure create_tables.sql is present."
        )

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
        conn.executescript(schema_sql)
        conn.commit()

    print(f"Database created or updated at: {DB_PATH}")


if __name__ == "__main__":
    main()
