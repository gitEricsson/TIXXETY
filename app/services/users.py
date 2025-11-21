from app.repositories.user_repo import UserRepository
from app.schemas.users import UserCreate, UserRead
from fastapi import HTTPException

class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def register_user(self, payload: UserCreate) -> UserRead:
        # prevent duplicate email
        existing = await self.repo.get_by_email(payload.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        user = await self.repo.create(name=payload.name, email=payload.email)
        return UserRead.model_validate(user)