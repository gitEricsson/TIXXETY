from fastapi import APIRouter
from app.controllers.events import router as events_router
from app.controllers.tickets import router as tickets_router
from app.controllers.foryou import router as foryou_router
from app.controllers.users import router as users_router

api_router = APIRouter()
api_router.include_router(events_router, prefix="/events", tags=["events"])
api_router.include_router(tickets_router, prefix="/tickets", tags=["tickets"])
api_router.include_router(foryou_router, prefix="/for-you", tags=["for-you"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
