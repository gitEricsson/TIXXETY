from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repositories.ticket_repo import TicketRepository
from app.repositories.event_repo import EventRepository
from app.schemas.tickets import TicketReserve, TicketRead
from app.core.config import settings
from app.tasks.tickets import schedule_ticket_expiration


class TicketService:
	def __init__(self, db: AsyncSession) -> None:
		self.db = db
		self.tickets = TicketRepository(db)
		self.events = EventRepository(db)

	async def reserve_ticket(self, payload: TicketReserve) -> TicketRead:
		event = await self.events.get(payload.event_id)
		if event is None:
			raise HTTPException(status_code=404, detail="Event not found")
		if event.tickets_sold >= event.total_tickets:
			raise HTTPException(status_code=400, detail="Event is sold out")

		ticket = await self.tickets.create(user_id=payload.user_id, event_id=payload.event_id)
		await self.events.increment_tickets_sold(event.id, 1)
		await self.db.commit()
		await self.db.refresh(ticket)

		# schedule expiration after TTL seconds
		schedule_ticket_expiration.delay(ticket.id, settings.ticket_reservation_ttl_seconds)
		return TicketRead.model_validate(ticket)

	async def pay_ticket(self, ticket_id: int) -> TicketRead:
		ticket = await self.tickets.get(ticket_id)
		if ticket is None:
			raise HTTPException(status_code=404, detail="Ticket not found")
		if ticket.status == "expired":
			raise HTTPException(status_code=400, detail="Ticket already expired")
		if ticket.status == "paid":
			return TicketRead.model_validate(ticket)

		await self.tickets.set_status(ticket_id, "paid")
		await self.db.commit()
		await self.db.refresh(ticket)
		return TicketRead.model_validate(ticket)
