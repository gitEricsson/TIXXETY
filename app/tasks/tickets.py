from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.core.config import settings
from app.celery_app import celery_app
from app.models.ticket import Ticket
from app.models.event import Event
from app.tasks.utils import apply_expiration

# Use sync engine inside Celery task for simplicity
engine = create_engine(settings.sync_database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


@celery_app.task
def schedule_ticket_expiration(ticket_id: int, delay_seconds: int) -> None:
	# This indirection allows ETA scheduling via countdown in Celery; here we just queue immediate check with countdown
	expire_ticket.apply_async(args=[ticket_id], countdown=delay_seconds)


@celery_app.task
def expire_ticket(ticket_id: int) -> None:
	session = SessionLocal()
	try:
		ticket = session.get(Ticket, ticket_id)
		if ticket is None:
			return
		event = session.get(Event, ticket.event_id)
		changed = apply_expiration(ticket, event)
		if changed:
			session.commit()
	finally:
		session.close()
