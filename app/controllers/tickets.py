from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.tickets import TicketReserve, TicketRead
from app.services.tickets import TicketService

router = APIRouter()


@router.post("/", response_model=TicketRead)
async def reserve_ticket(payload: TicketReserve, db: AsyncSession = Depends(get_db)) -> TicketRead:
	service = TicketService(db)
	ticket = await service.reserve_ticket(payload)
	return ticket


@router.post("/{ticket_id}/pay", response_model=TicketRead)
async def pay_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)) -> TicketRead:
	service = TicketService(db)
	return await service.pay_ticket(ticket_id)
