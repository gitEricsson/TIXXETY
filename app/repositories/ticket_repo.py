from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ticket import Ticket


class TicketRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get(self, ticket_id: int) -> Ticket | None:
        res = await self.db.execute(select(Ticket).where(Ticket.id == ticket_id))
        return res.scalar_one_or_none()

    async def create(self, user_id: int, event_id: int) -> Ticket:
        t = Ticket(user_id=user_id, event_id=event_id, status="reserved")
        self.db.add(t)
        await self.db.flush()
        await self.db.commit()
        await self.db.refresh(t)
        return t

    async def set_status(self, ticket_id: int, status: str) -> None:
        ticket = await self.get(ticket_id)
        if ticket is None:
            return
        ticket.status = status
        await self.db.flush()
        await self.db.commit()

    async def reserved_unpaid_ticket_ids(self) -> list[int]:
        res = await self.db.execute(select(Ticket.id).where(Ticket.status == "reserved"))
        return [row[0] for row in res.all()]

    async def get_by_user_id(self, user_id: int) -> list[Ticket]:
        res = await self.db.execute(select(Ticket).where(Ticket.user_id == user_id))
        return list(res.scalars().all())
