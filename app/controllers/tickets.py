from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.tickets import TicketReserve, TicketRead
from app.services.tickets import TicketService
from typing import List

router = APIRouter()


@router.post("/", response_model=TicketRead)
async def reserve_ticket(
    payload: TicketReserve, db: AsyncSession = Depends(get_db)
) -> TicketRead:
    service = TicketService(db)
    ticket = await service.reserve_ticket(payload)
    return ticket


@router.post("/{ticket_id}/pay", response_model=TicketRead)
async def pay_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)) -> TicketRead:
    service = TicketService(db)
    return await service.pay_ticket(ticket_id)


@router.get("/users/{user_id}", response_model=List[TicketRead])
async def get_user_tickets_history(
    user_id: int, db: AsyncSession = Depends(get_db)
) -> List[TicketRead]:
    service = TicketService(db)
    tickets = await service.get_user_tickets(user_id)
    return tickets
