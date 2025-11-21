from fastapi import APIRouter, Depends
from app.schemas.tickets import TicketReserve, TicketRead
from app.services.tickets import TicketService
from app.deps import get_ticket_service
from typing import List

router = APIRouter()


@router.post("/", response_model=TicketRead)
async def reserve_ticket(
    payload: TicketReserve, service: TicketService = Depends(get_ticket_service)
) -> TicketRead:
    return await service.reserve_ticket(payload)


@router.post("/{ticket_id}/pay", response_model=TicketRead)
async def pay_ticket(ticket_id: int, service: TicketService = Depends(get_ticket_service)) -> TicketRead:
    return await service.pay_ticket(ticket_id)


@router.get("/users/{user_id}", response_model=List[TicketRead])
async def get_user_tickets_history(
    user_id: int, service: TicketService = Depends(get_ticket_service)
) -> List[TicketRead]:
    return await service.get_user_tickets(user_id)
