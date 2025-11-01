from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.event_repo import EventRepository
from app.repositories.user_repo import UserRepository
from app.schemas.events import EventRead


class RecommendationService:
	def __init__(self, db: AsyncSession) -> None:
		self.db = db
		self.events = EventRepository(db)
		self.users = UserRepository(db)

	async def events_near_user(self, user_id: int | None, lat: float | None, lng: float | None) -> list[EventRead]:
		# In real app, user profile could store last known location; here, require query lat/lng if not provided
		if lat is None or lng is None:
			# fallback: return all for now
			items = await self.events.list_all()
			return [EventRead.model_validate(e) for e in items]
		items = await self.events.events_within_radius(lat=lat, lng=lng)
		return [EventRead.model_validate(e) for e in items]
