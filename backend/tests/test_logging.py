import json
import logging

import pytest

import app.logging_config as logging_config
from app.logging_config import (
    AUDIT_LOGGER_NAME,
    StructuredFormatter,
    log_scoring_request,
    setup_logging,
)


@pytest.fixture(autouse=True)
def reset_logging():
    logging_config._CONFIGURED = False
    setup_logging()
    yield
    logging.getLogger().handlers.clear()
    logging_config._CONFIGURED = False


def test_log_scoring_request_emits_structured_audit_fields(caplog):
    with caplog.at_level(logging.INFO, logger=AUDIT_LOGGER_NAME):
        log_scoring_request(
            request_id="550e8400-e29b-41d4-a716-446655440000",
            timestamp="2026-06-05T10:00:00+00:00",
            land_area=3.5,
            repayment_score=75,
            income_band="2-5L",
            final_score=70.0,
            reason_codes=["average_repayment", "medium_landholding", "mid_income_band"],
        )

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.audit_data["request_id"] == "550e8400-e29b-41d4-a716-446655440000"
    assert record.audit_data["timestamp"] == "2026-06-05T10:00:00+00:00"
    assert record.audit_data["land_area"] == 3.5
    assert record.audit_data["repayment_score"] == 75
    assert record.audit_data["income_band"] == "2-5L"
    assert record.audit_data["final_score"] == 70.0
    assert record.audit_data["reason_codes"] == [
        "average_repayment",
        "medium_landholding",
        "mid_income_band",
    ]


def test_log_scoring_request_outputs_json(caplog):
    with caplog.at_level(logging.INFO, logger=AUDIT_LOGGER_NAME):
        log_scoring_request(
            request_id="abc-123",
            timestamp="2026-06-05T10:00:00+00:00",
            land_area=1.0,
            repayment_score=50,
            income_band="<2L",
            final_score=40.0,
            reason_codes=["poor_repayment", "small_landholding", "low_income_band"],
        )

    payload = json.loads(StructuredFormatter().format(caplog.records[0]))
    assert payload["event"] == "scoring_request_processed"
    assert payload["request_id"] == "abc-123"
    assert payload["final_score"] == 40.0
    assert "crop_type" not in payload
