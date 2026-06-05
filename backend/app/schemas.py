from enum import Enum

from pydantic import BaseModel, Field, field_validator


class IncomeBand(str, Enum):
    UNDER_2L = "<2L"
    BETWEEN_2_5L = "2-5L"
    BETWEEN_5_10L = "5-10L"
    OVER_10L = ">10L"


class ScoreRequest(BaseModel):
    land_area_acres: float = Field(gt=0, description="Land area in acres; must be positive")
    crop_type: str = Field(description="Any non-empty crop label")
    repayment_history_score: float = Field(ge=0, le=100, description="Inclusive range 0 to 100")
    annual_income_band: IncomeBand

    @field_validator("crop_type")
    @classmethod
    def crop_type_not_blank(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("crop_type cannot be empty or whitespace")
        return value.strip()


class ScoreResponse(BaseModel):
    request_id: str
    score: float = Field(ge=0, le=100)
    reason_codes: list[str] = Field(min_length=3, max_length=3)
    timestamp: str
