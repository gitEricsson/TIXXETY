from datetime import datetime
from pydantic import BaseModel, Field


class TicketReserve(BaseModel):
	user_id: int
	event_id: int


class TicketRead(BaseModel):
	id: int
	user_id: int
	event_id: int
	status: str
	created_at: datetime

	class Config:
		from_attributes = True
