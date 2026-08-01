# Wealth Monitor — Learning Path

This app is built in **stages**. Each stage is a git tag.
Juniors can walk the history one lesson at a time.

## How to walk the stages

```bash
# List all teaching stages
git tag -l 'stage-*'

# Open a specific lesson (example: database)
git checkout stage-01-database

# Return to the completed showcase app
git checkout master
```

## Core idea

Wealth is **not** stored as one balance number.

```text
Net = Total Income − Total Expenses
```

Every rupee in or out is a **transaction**. Reports add incomes and subtract expenses.

## Stages

| Tag | What you learn | Demo (2–3 min) |
|-----|----------------|----------------|
| `stage-01-database` | Tables, relationships, seed data | Open `database/migrations/` and explain each table |
| `stage-02-backend-foundation` | Settings, DB connection, health API | Run API and open `/` |
| `stage-03-models-schemas` | ORM models + request/response shapes | Show model ↔ table mapping |
| `stage-04-auth` | Register, login, JWT | Register a user, call a protected route |
| `stage-05-reference-data` | Categories & parties (payment channels) | List Food/Salary and Cash/UPI |
| `stage-06-transactions` | Create / list / edit / soft-delete money entries | Add lunch expense + salary income |
| `stage-07-summary-reports` | How wealth is calculated | Show totals, by category, by month |
| `stage-08-frontend-shell` | Login UI, routing, API client | Login screen and protected pages |
| `stage-09-frontend-features` | Full clickable UI | Dashboard + transactions + reports |
| `stage-10-docker-deploy` | Run and deploy anywhere | `docker compose up --build` then open :3000 |

Deploy details: [DEPLOY.md](DEPLOY.md)

## Files to open first (stage 01)

1. `database/README.md` — design principles
2. `database/migrations/001_schema.sql` — table definitions
3. `database/migrations/002_seed.sql` — starter categories and parties
4. `database/diagrams/` — ER pictures

## Teaching tip for parties

In seed data, parties are **payment channels**: Cash, Wallet, Bank, UPI.
That keeps the first lesson simple for beginners.
