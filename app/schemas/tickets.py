from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class TicketReserve(BaseModel):
    user_id: int
    event_id: int


class TicketRead(BaseModel):
    id: int
    user_id: int
    event_id: int
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
