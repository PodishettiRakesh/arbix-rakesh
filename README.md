# Arbix Farmer Credit Scoring

End-to-end crop/land credit scoring application built for the Arbix AI Round 1 practical exercise. Python FastAPI backend + React (Vite) frontend with validation, rule-based explainability, audit logging, and tests.

## Time-box Proof

| Item | Detail |
| ---- | ------ |
| **Start time (IST)** | 2026-06-05, 15:47 IST |
| **End time (IST)** | 2026-06-05, 16:46 IST |
| **Approximate total implementation time** | ~60 minutes |
| **Remaining time (within 90-min box)** | Testing, verification, documentation, and repository cleanup |
| **First commit** | `8f3a90f` — backend scaffold |
| **Final commit** | `59188b7` — frontend UI polish |

> Times are based on first and last meaningful git commit timestamps (IST). Core implementation finished within ~60 minutes; the remaining time in the 90-minute window was used for validation and polish.

## What Was Completed

- [x] **Backend API** — FastAPI with `GET /health` and `POST /score`
- [x] **Validation** — Pydantic models + FastAPI 422 responses; frontend inline validation
- [x] **Logging** — Structured JSON audit logs per scoring request
- [x] **Tests** — 35 backend tests (schemas, scoring, logging, API endpoint, health)
- [x] **React UI** — Vite + React form with loading, inline errors, and score display

## What Was Skipped (and Why)

| Skipped | Reason |
| ------- | ------ |
| Database (SQLite/Postgres) | Prioritized core end-to-end flow within the 90-minute time-box |
| Docker / docker-compose | Optional bonus; focused on working API + UI first |

## Design Decisions & Tradeoffs

- **FastAPI** — Built-in request validation, automatic OpenAPI/Swagger docs, and fast local development.
- **Rule-based scoring** — Spec explicitly said ML was not required; rules are transparent, explainable, and easy to test.
- **Separated modules** — `schemas.py`, `scoring.py`, and `logging_config.py` keep API, business logic, and logging concerns isolated.
- **Structured audit logging** — JSON console logs capture scoring-relevant fields only: `request_id`, `timestamp`, `land_area`, `repayment_score`, `income_band`, `final_score`, and `reason_codes`. Crop label is excluded from audit output to keep logs focused on scoring inputs, per the spec's guidance to avoid unnecessary data in logs.
- **Port 8002** — Backend configured on port `8002` for local development.
- **Progressive commits** — Each phase (setup, models, scoring, logging, API, tests, frontend) committed separately for clear history.

## If Given 2 More Hours

- Add SQLite persistence for score request history
- Add Dockerfile / docker-compose for one-command startup
- Expand test coverage (edge cases, logging integration tests)
- Environment-based API URL in frontend (`.env`) instead of hardcoded localhost
- More configurable scoring rules or admin endpoint

## LLM / Tool Disclosure

| Tool | How it was used | What I reviewed/changed |
| ---- | --------------- | ------------------------ |
| **Cursor / Claude** | Project structure, phase planning, boilerplate generation | Verified scoring boundaries, capped score at 100, ensured 3 reason codes, ran all tests manually |
| **Official docs** | FastAPI validation, Pydantic v2, Vite + React setup | Confirmed 422 error shape for frontend inline errors |

See [LLM_NOTES.md](LLM_NOTES.md) for example prompts and a correction example.

## Prerequisites

- Python 3.10+
- Node.js 18+

## Project Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI app + POST /score
│   │   ├── schemas.py        # Pydantic request/response models
│   │   ├── scoring.py        # Rule-based scoring logic
│   │   └── logging_config.py # Structured audit logging
│   ├── tests/
│   │   ├── test_health.py
│   │   ├── test_schemas.py
│   │   ├── test_scoring.py
│   │   ├── test_logging.py
│   │   └── test_score.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Scoring form UI
│   │   ├── App.css
│   │   └── main.jsx
│   └── package.json
├── README.md
└── LLM_NOTES.md
```

## Quick Start

### 1. Backend (port 8002)

```bash
git clone https://github.com/PodishettiRakesh/arbix-rakesh.git
cd arbix-rakesh/backend

python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8002
```

### 2. Frontend (port 5173)

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173** and ensure the backend is running on **http://localhost:8002**.

## API

| Endpoint | Method | Description |
| -------- | ------ | ----------- |
| `/health` | GET | Health check |
| `/score` | POST | Calculate credit score |
| `/docs` | GET | Swagger UI |

### Example request

```bash
curl -X POST http://localhost:8002/score \
  -H "Content-Type: application/json" \
  -d "{\"land_area_acres\": 6, \"crop_type\": \"Rice\", \"repayment_history_score\": 90, \"annual_income_band\": \">10L\"}"
```

### Example response

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "score": 94.0,
  "reason_codes": ["good_repayment", "large_landholding", "high_income_band"],
  "timestamp": "2026-06-05T10:00:00+00:00"
}
```

### Scoring rules (summary)

| Component | Rule |
| --------- | ---- |
| Repayment | `repayment_history_score × 0.6` (max 60 pts) |
| Land | >5 ac → 20 pts, 2–5 ac → 10 pts, <2 ac → 5 pts |
| Income | `<2L`→5, `2-5L`→10, `5-10L`→15, `>10L`→20 |
| Final | `min(100, round(sum, 2))` |
| Reason codes | Always 3: repayment band, land band, income band |

## Run Tests

```bash
cd backend
pytest -v
```

## Phase Summary

| Phase | Scope | Status |
| ----- | ----- | ------ |
| 1 | Backend setup & test harness | Done |
| 2 | Data models & validation | Done |
| 3 | Rule-based scoring logic | Done |
| 4 | Audit logging | Done |
| 5 | `POST /score` API endpoint | Done |
| 6 | Score endpoint unit tests | Done |
| 7 | React frontend | Done |
| 8 | Documentation | Done |

## Contact

- **GitHub:** [@PodishettiRakesh](https://github.com/PodishettiRakesh)
