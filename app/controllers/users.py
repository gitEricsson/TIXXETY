from fastapi import APIRouter, Depends
from app.schemas.users import UserCreate, UserRead
from app.services.users import UserService
from app.deps import get_user_service

router = APIRouter()

@router.post("/", response_model=UserRead)
async def register_user(
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserRead:
    return await service.register_user(payload)