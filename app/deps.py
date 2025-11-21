from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.ticket_repo import TicketRepository
from app.repositories.event_repo import EventRepository
from app.repositories.user_repo import UserRepository
from app.services.tickets import TicketService
from app.services.events import EventService
from app.services.recommendations import RecommendationService
from app.services.users import UserService

async def get_ticket_repo(db: AsyncSession = Depends(get_db)):
    return TicketRepository(db)

async def get_event_repo(db: AsyncSession = Depends(get_db)):
    return EventRepository(db)

async def get_user_repo(db: AsyncSession = Depends(get_db)):
    return UserRepository(db)

async def get_ticket_service(
    tickets: TicketRepository = Depends(get_ticket_repo),
    events: EventRepository = Depends(get_event_repo),
):
    return TicketService(tickets, events)

async def get_event_service(repo: EventRepository = Depends(get_event_repo)):
    return EventService(repo)

async def get_user_service(repo: UserRepository = Depends(get_user_repo)):
	return UserService(repo)

async def get_recommendation_service(
    events: EventRepository = Depends(get_event_repo),
    users: UserRepository = Depends(get_user_repo),
):
    return RecommendationService(events, users)