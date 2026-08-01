# Deploy Wealth Monitor

## Local showcase (recommended for training)

Prerequisites: Docker Desktop (or Docker Engine + Compose).

```bash
docker compose up --build
```

Then open:

- App: http://localhost:3000
- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/api/v1/health

Stop with `Ctrl+C`, or `docker compose down`.

Reset database (wipes data):

```bash
docker compose down -v
docker compose up --build
```

---

## Cloud showcase on Render

Create three services from the Render dashboard.

### 1. PostgreSQL

1. New → PostgreSQL
2. Copy the **Internal Database URL** parts into API env vars:
   - host, port, database name, user, password

Apply schema once (from your laptop, using the **External** DB URL):

```bash
psql "<EXTERNAL_DATABASE_URL>" -f database/migrations/001_schema.sql
psql "<EXTERNAL_DATABASE_URL>" -f database/migrations/002_seed.sql
```

### 2. API (Web Service)

1. New → Web Service
2. Connect this GitHub repo
3. Settings:
   - **Root Directory:** `python_backend`
   - **Runtime:** Docker
   - **Dockerfile Path:** `Dockerfile`
4. Environment variables (match `.env.example`):

| Key | Example |
|-----|---------|
| `DATABASE_HOST` | from Render Postgres |
| `DATABASE_PORT` | `5432` |
| `DATABASE_NAME` | from Render Postgres |
| `DATABASE_USER` | from Render Postgres |
| `DATABASE_PASSWORD` | from Render Postgres |
| `JWT_SECRET_KEY` | long random string |
| `JWT_ALGORITHM` | `HS256` |
| `JWT_EXPIRE_MINUTES` | `1440` |
| `DEBUG` | `false` |
| `CORS_ORIGINS_RAW` | your static site URL, e.g. `https://wealth-monitor.onrender.com` |

After deploy, confirm `https://<api-service>.onrender.com/api/v1/health`.

### 3. Frontend (Static Site)

1. New → Static Site
2. Root Directory: `react_frontend`
3. Build command: `npm install && npm run build`
4. Publish directory: `dist`
5. Environment:

| Key | Value |
|-----|-------|
| `VITE_API_URL` | `https://<api-service>.onrender.com/api/v1` |

Open the static site URL and register a demo user.

---

## VPS fallback (Docker Compose)

On any Linux VPS with Docker:

```bash
git clone <your-repo-url>
cd wealth-monitor
docker compose up --build -d
```

Point a reverse proxy (Caddy/Nginx) at port `3000` for HTTPS.
Change `JWT_SECRET_KEY` in `docker-compose.yml` before public use.
