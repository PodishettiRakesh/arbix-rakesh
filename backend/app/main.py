from contextlib import asynccontextmanager
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.logging_config import log_scoring_request, setup_logging
from app.schemas import ScoreRequest, ScoreResponse
from app.scoring import calculate_score


@asynccontextmanager
async def lifespan(_: FastAPI):
    setup_logging()
    yield


app = FastAPI(title="Arbix Scoring API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/score", response_model=ScoreResponse)
def score(request: ScoreRequest) -> ScoreResponse:
    request_id = str(uuid4())
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    result = calculate_score(request)

    log_scoring_request(
        request_id=request_id,
        timestamp=timestamp,
        land_area=request.land_area_acres,
        repayment_score=request.repayment_history_score,
        income_band=request.annual_income_band.value,
        final_score=result.score,
        reason_codes=result.reason_codes,
    )

    return ScoreResponse(
        request_id=request_id,
        score=result.score,
        reason_codes=result.reason_codes,
        timestamp=timestamp,
    )
