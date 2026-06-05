import pytest
from fastapi.testclient import TestClient

from app.database import init_db
from app.main import app


@pytest.fixture(autouse=True)
def test_database(tmp_path, monkeypatch):
    db_path = tmp_path / "test_scores.db"
    monkeypatch.setenv("SCORES_DB_PATH", str(db_path))
    init_db(db_path)


@pytest.fixture
def client():
    return TestClient(app)
