# Wealth Monitor

A full-stack personal finance tracker used to **teach juniors** how a real app is built.

Stack:

- React + Vite + MUI
- Python FastAPI
- PostgreSQL

## Features (showcase)

- User registration and login (JWT)
- Income and expense tracking
- Categories and payment channels
- Dashboard summary (income / expense / net)
- Reports by category and by month

## Architecture

```text
Frontend → Backend API → PostgreSQL
```

Wealth is calculated, not stored:

```text
Net = Total Income − Total Expenses
```

## Quick start (Docker)

```bash
docker compose up --build
```

- App: http://localhost:3000
- API docs: http://localhost:8000/docs

See [DEPLOY.md](DEPLOY.md) for cloud deploy (Render) and VPS notes.

## Teaching stages

This repo is built as tagged lessons. Instructors and juniors can walk history:

```bash
git tag -l 'stage-*'
git checkout stage-01-database
# ...study the lesson...
git checkout master   # completed showcase
```

Full lesson map: [LEARNING.md](LEARNING.md)

## Local development (without Docker)

### Database

Apply migrations to a local Postgres database named `wealth_monitor`:

```bash
psql -U postgres -d wealth_monitor -f database/migrations/001_schema.sql
psql -U postgres -d wealth_monitor -f database/migrations/002_seed.sql
```

### Backend

```bash
cd python_backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

### Frontend

Requires Node.js 20.19+ or 22.12+ (Docker image already uses Node 22).

```bash
cd react_frontend
npm install
cp .env.example .env
npm run dev
```

## Developed by

C - VERSE

Training / personal-use demo application.
