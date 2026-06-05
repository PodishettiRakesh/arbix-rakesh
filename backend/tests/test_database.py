import pytest

from app.database import get_score_record, init_db, save_score_record
from app.schemas import IncomeBand, ScoreRequest


@pytest.fixture
def db_path(tmp_path):
    path = tmp_path / "test_scores.db"
    init_db(path)
    return path


def make_request() -> ScoreRequest:
    return ScoreRequest(
        land_area_acres=3.5,
        crop_type="wheat",
        repayment_history_score=75,
        annual_income_band=IncomeBand.BETWEEN_2_5L,
    )


def test_save_and_get_score_record(db_path):
    request = make_request()
    save_score_record(
        request_id="test-id-123",
        timestamp="2026-06-05T10:00:00+00:00",
        request=request,
        score=70.0,
        reason_codes=["average_repayment", "medium_landholding", "mid_income_band"],
        db_path=db_path,
    )

    record = get_score_record("test-id-123", db_path=db_path)

    assert record is not None
    assert record["request_id"] == "test-id-123"
    assert record["score"] == 70.0
    assert record["crop_type"] == "wheat"
    assert record["annual_income_band"] == "2-5L"
    assert record["reason_codes"] == [
        "average_repayment",
        "medium_landholding",
        "mid_income_band",
    ]


def test_get_score_record_returns_none_for_missing_id(db_path):
    assert get_score_record("missing-id", db_path=db_path) is None
