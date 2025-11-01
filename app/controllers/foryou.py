from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.events import EventRead
from app.services.recommendations import RecommendationService

router = APIRouter()


@router.get("/", response_model=list[EventRead])
async def for_you(
	user_id: int | None = Query(default=None),
	lat: float | None = Query(default=None),
	lng: float | None = Query(default=None),
	db: AsyncSession = Depends(get_db),
) -> list[EventRead]:
	service = RecommendationService(db)
	return await service.events_near_user(user_id=user_id, lat=lat, lng=lng)
