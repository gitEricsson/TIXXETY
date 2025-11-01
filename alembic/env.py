from __future__ import annotations
from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from app.db.session import Base

# Add project root to path so we can import app
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables from .env file
load_dotenv(project_root / ".env")


config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Default to localhost for local dev, but allow override via environment variable
# For Docker, set SYNC_DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/tixxety
DB_URL = os.getenv(
    "SYNC_DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/tixxety"
)


def run_migrations_offline() -> None:
    url = DB_URL
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(DB_URL)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
