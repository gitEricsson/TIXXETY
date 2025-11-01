from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from app.models.event import Event


class EventRepository:
	def __init__(self, db: AsyncSession) -> None:
		self.db = db

	async def list_all(self) -> list[Event]:
		res = await self.db.execute(select(Event))
		return list(res.scalars().all())

	async def create(
		self,
		title: str,
		description: str | None,
		start_time,
		end_time,
		total_tickets: int,
		venue_address: str,
		lat: float,
		lng: float,
	) -> Event:
		point = from_shape(Point(lng, lat), srid=4326)
		event = Event(
			title=title,
			description=description,
			start_time=start_time,
			end_time=end_time,
			total_tickets=total_tickets,
			tickets_sold=0,
			venue_address=venue_address,
			venue_location=point,
		)
		self.db.add(event)
		await self.db.flush()
		return event

	async def get(self, event_id: int) -> Event | None:
		res = await self.db.execute(select(Event).where(Event.id == event_id))
		return res.scalar_one_or_none()

	async def increment_tickets_sold(self, event_id: int, inc: int = 1) -> None:
		event = await self.get(event_id)
		if event is None:
			return
		event.tickets_sold = (event.tickets_sold or 0) + inc
		await self.db.flush()

	async def events_within_radius(self, lat: float, lng: float, radius_km: float = 25.0) -> list[Event]:
		# Use ST_DWithin with geography to get events within radius in meters
		meters = radius_km * 1000.0
		q = (
			select(Event)
			.where(
				func.ST_DWithin(
					Event.venue_location, func.ST_SetSRID(func.ST_Point(lng, lat), 4326), meters
				)
			)
			.order_by(
				func.ST_Distance(
					Event.venue_location, func.ST_SetSRID(func.ST_Point(lng, lat), 4326)
				)
			)
		)
		res = await self.db.execute(q)
		return list(res.scalars().all())
