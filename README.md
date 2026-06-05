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

## Phase 7 — Frontend (current)

React + Vite UI in `frontend/` with a scoring form, loading/error states, and score + reason code display.

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
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```

API base URL: `http://localhost:8002`

- Health check: `GET http://localhost:8002/health`
- Score endpoint: `POST http://localhost:8002/score`
- Interactive docs: `http://localhost:8002/docs`

### Example `POST /score` request

```bash
curl -X POST http://localhost:8002/score \
  -H "Content-Type: application/json" \
  -d "{\"land_area_acres\": 6, \"crop_type\": \"wheat\", \"repayment_history_score\": 85, \"annual_income_band\": \"2-5L\"}"
```

## Run the Frontend

From the `frontend/` directory:

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:5173`

Make sure the backend is running on port `8002` before submitting the form.

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
| 4 | Audit logging (`logging_config.py`) | Done |
| 5 | `POST /score` API endpoint | Done |
| 6 | Score endpoint unit tests | Done |
| 7 | React frontend | Done |
| 8 | Documentation (`LLM_NOTES.md`, time-box proof) |

## Contact

- **GitHub:** [@PodishettiRakesh](https://github.com/PodishettiRakesh)
