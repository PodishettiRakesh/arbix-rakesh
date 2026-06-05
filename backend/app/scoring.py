from dataclasses import dataclass

from app.schemas import IncomeBand, ScoreRequest


@dataclass
class ScoreResult:
    score: float
    reason_codes: list[str]


def _land_component(land_area_acres: float) -> tuple[int, str]:
    if land_area_acres > 5:
        return 20, "large_landholding"
    if land_area_acres >= 2:
        return 10, "medium_landholding"
    return 5, "small_landholding"


def _income_component(income_band: IncomeBand) -> tuple[int, str]:
    mapping = {
        IncomeBand.UNDER_2L: (5, "low_income_band"),
        IncomeBand.BETWEEN_2_5L: (10, "mid_income_band"),
        IncomeBand.BETWEEN_5_10L: (15, "upper_mid_income_band"),
        IncomeBand.OVER_10L: (20, "high_income_band"),
    }
    return mapping[income_band]


def _repayment_reason(score: float) -> str:
    if score >= 80:
        return "good_repayment"
    if score >= 50:
        return "average_repayment"
    return "poor_repayment"


def calculate_score(data: ScoreRequest) -> ScoreResult:
    repayment_points = data.repayment_history_score * 0.6
    land_points, land_reason = _land_component(data.land_area_acres)
    income_points, income_reason = _income_component(data.annual_income_band)

    score = min(100, round(repayment_points + land_points + income_points, 2))
    repayment_reason = _repayment_reason(score)

    return ScoreResult(
        score=score,
        reason_codes=[repayment_reason, land_reason, income_reason],
    )
