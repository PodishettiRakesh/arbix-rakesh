# Arbix Scoring Application

End-to-end crop/land scoring application with a Python FastAPI backend and a React frontend (Arbix AI practical exercise).

## Prerequisites

- Python 3.10+
- Node.js 18+ (for frontend, Phase 7+)

## Project Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI app entry point (Phase 1)
│   │   ├── schemas.py        # Pydantic models (Phase 2)
│   │   ├── scoring.py        # Rule-based scoring logic (Phase 3)
│   │   └── logging_config.py # Audit logging setup (Phase 4)
│   ├── tests/
│   └── requirements.txt
├── frontend/                 # React UI (Phase 7)
└── README.md
```

## Phase 3 — Scoring Logic (current)

Rule-based scoring lives in `backend/app/scoring.py` via `calculate_score()`. Audit logging and the `/score` API endpoint come in later phases.

## Backend Setup

```bash
git clone https://github.com/PodishettiRakesh/arbix-rakesh.git
cd arbix-rakesh/backend

python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

## Run the Backend

From the `backend/` directory:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API base URL: `http://localhost:8000`

- Health check: `GET http://localhost:8000/health`
- Interactive docs: `http://localhost:8000/docs`

## Run Tests

From the `backend/` directory:

```bash
pytest -v
```

## Upcoming Phases

| Phase | Scope | Status |
| ----- | ----- | ------ |
| 1 | Backend setup & test harness | Done |
| 2 | Data models & validation (`schemas.py`) | Done |
| 3 | Rule-based scoring logic (`scoring.py`) | Done |
| 4 | Audit logging (`logging_config.py`) |
| 5 | `POST /score` API endpoint |
| 6 | Score endpoint unit tests |
| 7 | React frontend |
| 8 | Documentation (`LLM_NOTES.md`, time-box proof) |

## Contact

- **GitHub:** [@PodishettiRakesh](https://github.com/PodishettiRakesh)
