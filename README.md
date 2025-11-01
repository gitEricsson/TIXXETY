# TIXXETY

FastAPI-based ticketing API with clean architecture, async SQLAlchemy (PostgreSQL + PostGIS), Alembic migrations, Celery background worker for expiring unpaid tickets, and geospatial event recommendations.

## Stack

- FastAPI, Uvicorn
- Async SQLAlchemy 2.0, Alembic
- PostgreSQL with PostGIS (geospatial)
- Celery + Redis (broker + result backend)
- Pytest
- Docker Compose

## Features

- Create and list events with venue (address + location)
- Reserve and pay for tickets
- Auto-expire unpaid tickets after 2 minutes via Celery
- For-you feed: events near a user using geospatial query
- Class-based clean architecture (controllers, services, repositories, schemas, models, routes, utils)
- Logging, middleware, dependency injection, Singleton pattern for settings

## Quickstart

```bash
# 1) Start stack
docker compose up --build -d

# 2) Initialize DB and run migrations
docker compose exec api alembic upgrade head

# 3) API docs
# Visit http://localhost:8000/docs
```

## Local Dev (optional)

**Prerequisites:** Make sure PostgreSQL with PostGIS is running locally on port 5432, or update `SYNC_DATABASE_URL` in your environment.

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
cp env.example .env  # Copy and edit .env with your settings
alembic upgrade head
uvicorn app.main:app --reload
```

## Tests

```bash
pytest -q
```

## Environment

Copy `env.example` to `.env` and adjust for your setup. See `env.example` for all configuration options. Defaults wired for Docker network:

- DB: `postgresql+psycopg://postgres:postgres@db:5432/tixxety` (Docker) or `localhost:5432` (local dev)
- Redis: `redis://redis:6379/0`

**Note:** When running locally (outside Docker), migrations default to `localhost:5432`. Set `SYNC_DATABASE_URL` environment variable to override.
