import json
import os
import sqlite3
from pathlib import Path

from app.schemas import ScoreRequest

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "scores.db"


def get_db_path() -> Path:
    configured = os.environ.get("SCORES_DB_PATH")
    if configured:
        return Path(configured)
    return DEFAULT_DB_PATH


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or get_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def init_db(db_path: Path | None = None) -> None:
    with get_connection(db_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS score_records (
                request_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                land_area_acres REAL NOT NULL,
                crop_type TEXT NOT NULL,
                repayment_history_score REAL NOT NULL,
                annual_income_band TEXT NOT NULL,
                score REAL NOT NULL,
                reason_codes TEXT NOT NULL
            )
            """
        )
        connection.commit()


def save_score_record(
    *,
    request_id: str,
    timestamp: str,
    request: ScoreRequest,
    score: float,
    reason_codes: list[str],
    db_path: Path | None = None,
) -> None:
    with get_connection(db_path) as connection:
        connection.execute(
            """
            INSERT INTO score_records (
                request_id,
                timestamp,
                land_area_acres,
                crop_type,
                repayment_history_score,
                annual_income_band,
                score,
                reason_codes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                request_id,
                timestamp,
                request.land_area_acres,
                request.crop_type,
                request.repayment_history_score,
                request.annual_income_band.value,
                score,
                json.dumps(reason_codes),
            ),
        )
        connection.commit()


def get_score_record(request_id: str, db_path: Path | None = None) -> dict | None:
    with get_connection(db_path) as connection:
        row = connection.execute(
            "SELECT * FROM score_records WHERE request_id = ?",
            (request_id,),
        ).fetchone()

    if row is None:
        return None

    return {
        "request_id": row["request_id"],
        "timestamp": row["timestamp"],
        "land_area_acres": row["land_area_acres"],
        "crop_type": row["crop_type"],
        "repayment_history_score": row["repayment_history_score"],
        "annual_income_band": row["annual_income_band"],
        "score": row["score"],
        "reason_codes": json.loads(row["reason_codes"]),
    }
