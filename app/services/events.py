from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.event_repo import EventRepository
from app.schemas.events import EventCreate, EventRead


class EventService:
	def __init__(self, db: AsyncSession) -> None:
		self.db = db
		self.repo = EventRepository(db)

	async def create_event(self, payload: EventCreate) -> EventRead:
		event = await self.repo.create(
			title=payload.title,
			description=payload.description,
			start_time=payload.start_time,
			end_time=payload.end_time,
			total_tickets=payload.total_tickets,
			venue_address=payload.venue.address,
			lat=payload.venue.lat,
			lng=payload.venue.lng,
		)
		await self.db.commit()
		await self.db.refresh(event)
		return EventRead.model_validate(event)

	async def list_events(self) -> list[EventRead]:
		items = await self.repo.list_all()
		return [EventRead.model_validate(e) for e in items]
