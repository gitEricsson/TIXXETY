# TIXXETY

FastAPI-based ticketing API with clean architecture, async SQLAlchemy (PostgreSQL + PostGIS), Alembic migrations, Celery background worker for expiring unpaid tickets, and geospatial event recommendations.

## Stack

- FastAPI, Uvicorn
- Async SQLAlchemy 2.0, Alembic
- PostgreSQL with PostGIS (geospatial)
- Celery + Redis (broker + result backend)
- Pytest, httpx, pytest-asyncio
- Docker Compose

## Features

- Create and list events with venue (address + location)
- Reserve and pay for tickets
- **Fetch user ticket history**
- Auto-expire unpaid tickets after 2 minutes via Celery
- For-you feed: events near a user using geospatial query
- Class-based clean architecture (controllers, services, repositories, schemas, models, routes, utils)
- Logging, middleware, dependency injection, Singleton pattern for settings

## Quickstart (Docker)

This is the recommended way to run the application, as it sets up all services (API, PostgreSQL, Redis, Celery) automatically.

```bash
# 1) Start the entire stack (API, DB, Redis, Celery)
docker compose up --build -d

# 2) Initialize DB and run Alembic migrations
# This will create all necessary tables in your PostgreSQL database.
docker compose exec api alembic upgrade head

# 3) API docs
# Once the services are up, visit http://localhost:8000/docs for the API documentation.
```

## Local Development (optional)

If you prefer to run the application directly on your machine:

**Prerequisites:**

- Python 3.9+
- PostgreSQL with PostGIS extension enabled, running locally on port `5432`.
- Redis server running locally on port `6379`.

**Setup Steps:**

```bash
# 1) Create and activate a Python virtual environment
python -m venv .venv
. .venv/bin/activate # On Windows, use `.venv\Scripts\activate`

# 2) Install dependencies
pip install -r requirements.txt

# 3) Configure environment variables
# Copy the example environment file and edit it.
# IMPORTANT: Update SYNC_DATABASE_URL with your PostgreSQL password
# and ensure other URLs point to your local services (localhost).
cp env.example .env

# 4) Run Alembic migrations
# This will set up your local database schema.
alembic upgrade head

# 5) Run the FastAPI application
uvicorn app.main:app --reload

# 6) (Optional) To run the Celery worker for ticket expiration
# Open a new terminal, activate your virtual environment, and run:
celery -A app.celery_app worker -l info
```

## Tests

### Unit Tests

To run the unit tests (using `pytest` and `pytest-asyncio`):

```bash
# From the project root
pytest -q
```

### End-to-End (E2E) Test Data Setup

To prepare your local PostgreSQL database with sample data for E2E testing:

**WARNING:** This script will **DROP ALL EXISTING TABLES AND DATA** in your configured database before reseeding. Only run this on a development database where data loss is acceptable.

```bash
# From the project root, with your virtual environment active
python scripts/seed_db.py
```

After running this script, you can interact with your API endpoints (e.g., `/tickets/users/{user_id}`) to test the application with pre-populated data.

## Environment

Configuration is managed via environment variables. Copy `env.example` to `.env` and adjust settings as needed.

Key environment variables:

- `SYNC_DATABASE_URL`: Database connection string. Defaults to `postgresql+psycopg://postgres:postgres@localhost:5432/tixxety` if not set, but Docker compose uses `db:5432`. **Ensure you update this in `.env` with your correct PostgreSQL password.**
- `REDIS_URL`: Redis connection string for caching and task queue.
- `CELERY_BROKER_URL`: URL for the Celery message broker (Redis).
- `CELERY_RESULT_BACKEND`: URL for the Celery result backend (Redis).

**Note on Docker vs. Local:** When running locally, ensure `SYNC_DATABASE_URL` and `REDIS_URL` point to `localhost`. When using Docker Compose, these automatically point to the service names (`db` and `redis`).

API addition

- POST /users — register a user (accepts UserCreate, returns UserRead). Controllers/services/repositories follow DI: controllers depend on service interfaces; services depend on repository interfaces.

Tests

- Unit tests were updated to construct services with repository fakes (e.g. TicketService(tickets_repo, events_repo)). If you have custom tests that instantiated services with a DB/session, update them to pass repository fakes or use the dependency providers in tests.

Seed script

- scripts/seed_db.py now uses the async engine and creates events using proper start_time/end_time and PostGIS venue_location.

Run tests

- From project root on Windows:
  .venv\Scripts\activate
  pip install -r requirements.txt
  pytest -q
