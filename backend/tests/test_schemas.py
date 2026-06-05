import pytest
from pydantic import ValidationError

from app.schemas import IncomeBand, ScoreRequest, ScoreResponse


def valid_request_kwargs():
    return {
        "land_area_acres": 3.5,
        "crop_type": "wheat",
        "repayment_history_score": 75,
        "annual_income_band": IncomeBand.BETWEEN_2_5L,
    }


def test_score_request_valid():
    request = ScoreRequest(**valid_request_kwargs())
    assert request.land_area_acres == 3.5
    assert request.crop_type == "wheat"
    assert request.repayment_history_score == 75
    assert request.annual_income_band == IncomeBand.BETWEEN_2_5L


def test_score_request_strips_crop_type_whitespace():
    request = ScoreRequest(**{**valid_request_kwargs(), "crop_type": "  rice  "})
    assert request.crop_type == "rice"


@pytest.mark.parametrize(
    "overrides",
    [
        {"land_area_acres": 0},
        {"land_area_acres": -1},
        {"crop_type": ""},
        {"crop_type": "   "},
        {"repayment_history_score": -1},
        {"repayment_history_score": 101},
        {"annual_income_band": "invalid_band"},
    ],
)
def test_score_request_validation_errors(overrides):
    with pytest.raises(ValidationError):
        ScoreRequest(**{**valid_request_kwargs(), **overrides})


def test_score_response_valid():
    response = ScoreResponse(
        request_id="550e8400-e29b-41d4-a716-446655440000",
        score=72.5,
        reason_codes=["good_repayment", "medium_landholding", "mid_income_band"],
        timestamp="2026-06-05T10:00:00+00:00",
    )
    assert response.score == 72.5
    assert len(response.reason_codes) == 3


@pytest.mark.parametrize("reason_codes", [[], ["one"], ["one", "two"], ["a", "b", "c", "d"]])
def test_score_response_requires_exactly_three_reason_codes(reason_codes):
    with pytest.raises(ValidationError):
        ScoreResponse(
            request_id="550e8400-e29b-41d4-a716-446655440000",
            score=50,
            reason_codes=reason_codes,
            timestamp="2026-06-05T10:00:00+00:00",
        )
