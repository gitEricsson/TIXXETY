from app.repositories.event_repo import EventRepository
from app.repositories.user_repo import UserRepository
from app.schemas.events import EventRead


class RecommendationService:
    def __init__(self, events: EventRepository, users: UserRepository) -> None:
        self.events = events
        self.users = users

    async def events_near_user(self, user_id: int | None, lat: float | None, lng: float | None) -> list[EventRead]:
        if lat is None or lng is None:
            items = await self.events.list_all()
            return [EventRead.model_validate(e) for e in items]
        items = await self.events.events_within_radius(lat=lat, lng=lng)
        return [EventRead.model_validate(e) for e in items]
