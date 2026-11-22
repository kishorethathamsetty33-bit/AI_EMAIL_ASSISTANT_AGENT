
import sqlite3

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "email_assistant.db"


def get_connection():

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(
        str(DATABASE_PATH),
        timeout=10
    )

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    with get_connection() as connection:

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS drafts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                original_input TEXT NOT NULL,
                subject TEXT,
                body TEXT,
                category TEXT,
                reason TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.commit()


def save_draft(
    action,
    original_input,
    subject="",
    body="",
    category="",
    reason=""
):

    with get_connection() as connection:

        cursor = connection.execute(
            """
            INSERT INTO drafts (
                action,
                original_input,
                subject,
                body,
                category,
                reason
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                action,
                original_input,
                subject,
                body,
                category,
                reason,
            )
        )

        connection.commit()

        return cursor.lastrowid


def get_all_drafts():

    with get_connection() as connection:

        rows = connection.execute(
            """
            SELECT *
            FROM drafts
            ORDER BY id DESC
            """
        ).fetchall()

        return [dict(row) for row in rows]


def get_draft_by_id(draft_id):

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT *
            FROM drafts
            WHERE id = ?
            """,
            (draft_id,)
        ).fetchone()

        return dict(row) if row else None
