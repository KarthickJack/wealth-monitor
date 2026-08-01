# Wealth Monitor — Python Backend

FastAPI API for the Wealth Monitor training app.

## Setup

```bash
cd python_backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Apply database migrations first (see `../database/README.md`), then run:

```bash
uvicorn app.main:app --reload --port 8000
```

- Health: http://localhost:8000/api/v1/health
- Docs: http://localhost:8000/docs

## Folder map (for juniors)

| Folder | Job |
|--------|-----|
| `routers/` | HTTP endpoints |
| `services/` | Business rules |
| `repositories/` | Database queries |
| `models/` | SQLAlchemy tables |
| `schemas/` | Request/response shapes |
| `core/` | Settings, security, constants |
| `db/` | Engine and session |
