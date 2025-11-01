"""init models

Revision ID: 0001_init
Revises: 
Create Date: 2025-10-31

"""
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geography

# revision identifiers, used by Alembic.
revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
    )
    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.String(length=2000), nullable=True),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("total_tickets", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("tickets_sold", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("venue_address", sa.String(length=400), nullable=False),
        sa.Column("venue_location", Geography(geometry_type="POINT", srid=4326, spatial_index=True), nullable=False),
    )
    op.create_index("ix_events_id", "events", ["id"], unique=False)

    op.create_table(
        "tickets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("event_id", sa.Integer(), sa.ForeignKey("events.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="reserved"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_tickets_id", "tickets", ["id"], unique=False)
    op.create_index("ix_tickets_user_id", "tickets", ["user_id"], unique=False)
    op.create_index("ix_tickets_event_id", "tickets", ["event_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_tickets_event_id", table_name="tickets")
    op.drop_index("ix_tickets_user_id", table_name="tickets")
    op.drop_index("ix_tickets_id", table_name="tickets")
    op.drop_table("tickets")

    op.drop_index("ix_events_id", table_name="events")
    op.drop_table("events")

    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")


