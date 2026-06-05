import json
import logging
import sys

AUDIT_LOGGER_NAME = "audit"

_CONFIGURED = False


class StructuredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict = {
            "level": record.levelname,
            "logger": record.name,
            "event": record.getMessage(),
        }
        audit_data = getattr(record, "audit_data", None)
        if audit_data:
            payload.update(audit_data)
        return json.dumps(payload, default=str)


def setup_logging(level: int = logging.INFO) -> None:
    global _CONFIGURED
    root = logging.getLogger()
    if _CONFIGURED and root.handlers:
        return

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(StructuredFormatter())

    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    setup_logging()
    return logging.getLogger(name)


def log_scoring_request(
    *,
    request_id: str,
    timestamp: str,
    land_area: float,
    repayment_score: float,
    income_band: str,
    final_score: float,
    reason_codes: list[str],
) -> None:
    """Log a scoring request for audit. Only non-sensitive scoring fields are recorded."""
    logger = get_logger(AUDIT_LOGGER_NAME)
    logger.info(
        "scoring_request_processed",
        extra={
            "audit_data": {
                "request_id": request_id,
                "timestamp": timestamp,
                "land_area": land_area,
                "repayment_score": repayment_score,
                "income_band": income_band,
                "final_score": final_score,
                "reason_codes": reason_codes,
            }
        },
    )
