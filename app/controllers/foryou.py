from fastapi import APIRouter, Depends, Query
from app.schemas.events import EventRead
from app.services.recommendations import RecommendationService
from app.deps import get_recommendation_service

router = APIRouter()


@router.get("/", response_model=list[EventRead])
async def for_you(
	user_id: int | None = Query(default=None),
	lat: float | None = Query(default=None),
	lng: float | None = Query(default=None),
	service: RecommendationService = Depends(get_recommendation_service),
) -> list[EventRead]:
	return await service.events_near_user(user_id=user_id, lat=lat, lng=lng)
