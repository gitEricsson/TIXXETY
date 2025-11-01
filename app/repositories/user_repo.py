from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User


class UserRepository:
	def __init__(self, db: AsyncSession) -> None:
		self.db = db

	async def get(self, user_id: int) -> User | None:
		res = await self.db.execute(select(User).where(User.id == user_id))
		return res.scalar_one_or_none()

	async def get_by_email(self, email: str) -> User | None:
		res = await self.db.execute(select(User).where(User.email == email))
		return res.scalar_one_or_none()

	async def create(self, name: str, email: str) -> User:
		user = User(name=name, email=email)
		self.db.add(user)
		await self.db.flush()
		return user
