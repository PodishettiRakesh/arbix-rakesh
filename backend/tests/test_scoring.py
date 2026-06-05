import pytest

from app.schemas import IncomeBand, ScoreRequest
from app.scoring import calculate_score


def make_request(**overrides) -> ScoreRequest:
    defaults = {
        "land_area_acres": 3.5,
        "crop_type": "wheat",
        "repayment_history_score": 75,
        "annual_income_band": IncomeBand.BETWEEN_2_5L,
    }
    return ScoreRequest(**{**defaults, **overrides})


def test_calculate_score_high_scoring_profile():
    result = calculate_score(
        make_request(
            land_area_acres=6,
            repayment_history_score=100,
            annual_income_band=IncomeBand.OVER_10L,
        )
    )

    assert result.score == 100
    assert result.reason_codes == ["good_repayment", "large_landholding", "high_income_band"]


def test_calculate_score_low_scoring_profile():
    result = calculate_score(
        make_request(
            land_area_acres=1,
            repayment_history_score=10,
            annual_income_band=IncomeBand.UNDER_2L,
        )
    )

    assert result.score == 16.0
    assert result.reason_codes == ["poor_repayment", "small_landholding", "low_income_band"]


@pytest.mark.parametrize(
    ("land_area", "expected_reason"),
    [
        (6, "large_landholding"),
        (5, "medium_landholding"),
        (2, "medium_landholding"),
        (1.9, "small_landholding"),
    ],
)
def test_land_component_boundaries(land_area, expected_reason):
    result = calculate_score(make_request(land_area_acres=land_area))
    assert result.reason_codes[1] == expected_reason


@pytest.mark.parametrize(
    ("income_band", "expected_reason"),
    [
        (IncomeBand.UNDER_2L, "low_income_band"),
        (IncomeBand.BETWEEN_2_5L, "mid_income_band"),
        (IncomeBand.BETWEEN_5_10L, "upper_mid_income_band"),
        (IncomeBand.OVER_10L, "high_income_band"),
    ],
)
def test_income_component_reasons(income_band, expected_reason):
    result = calculate_score(make_request(annual_income_band=income_band))
    assert result.reason_codes[2] == expected_reason


@pytest.mark.parametrize(
    ("overrides", "expected_repayment_reason"),
    [
        (
            {
                "land_area_acres": 6,
                "repayment_history_score": 100,
                "annual_income_band": IncomeBand.OVER_10L,
            },
            "good_repayment",
        ),
        (
            {
                "land_area_acres": 3,
                "repayment_history_score": 50,
                "annual_income_band": IncomeBand.BETWEEN_2_5L,
            },
            "average_repayment",
        ),
        (
            {
                "land_area_acres": 1,
                "repayment_history_score": 0,
                "annual_income_band": IncomeBand.UNDER_2L,
            },
            "poor_repayment",
        ),
    ],
)
def test_repayment_reason_from_final_score(overrides, expected_repayment_reason):
    result = calculate_score(make_request(**overrides))
    assert result.reason_codes[0] == expected_repayment_reason


def test_score_is_capped_at_100():
    result = calculate_score(
        make_request(
            land_area_acres=10,
            repayment_history_score=100,
            annual_income_band=IncomeBand.OVER_10L,
        )
    )
    assert result.score == 100


def test_always_returns_exactly_three_reason_codes():
    result = calculate_score(make_request())
    assert len(result.reason_codes) == 3
