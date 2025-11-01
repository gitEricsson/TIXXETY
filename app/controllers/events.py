from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.events import EventCreate, EventRead
from app.services.events import EventService

router = APIRouter()


@router.post("/", response_model=EventRead)
async def create_event(payload: EventCreate, db: AsyncSession = Depends(get_db)) -> EventRead:
	service = EventService(db)
	return await service.create_event(payload)


@router.get("/", response_model=list[EventRead])
async def list_events(db: AsyncSession = Depends(get_db)) -> list[EventRead]:
	service = EventService(db)
	return await service.list_events()
