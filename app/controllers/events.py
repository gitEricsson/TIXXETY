from fastapi import APIRouter, Depends
from app.schemas.events import EventCreate, EventRead
from app.services.events import EventService
from app.deps import get_event_service

router = APIRouter()


@router.post("/", response_model=EventRead)
async def create_event(
    payload: EventCreate,
    service: EventService = Depends(get_event_service),
) -> EventRead:
    return await service.create_event(payload)


@router.get("/", response_model=list[EventRead])
async def list_events(
    service: EventService = Depends(get_event_service),
) -> list[EventRead]:
    return await service.list_events()
