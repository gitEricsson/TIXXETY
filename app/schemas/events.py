from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict


class Venue(BaseModel):
    address: str = Field(..., min_length=1)
    lat: float
    lng: float


class EventBase(BaseModel):
    title: str
    description: str | None = None
    start_time: datetime
    end_time: datetime
    total_tickets: int = Field(ge=0)
    venue: Venue

    @field_validator("end_time")
    @classmethod
    def validate_times(cls, v: datetime, info):
        start = info.data.get("start_time")
        if start and v <= start:
            raise ValueError("end_time must be after start_time")
        return v


class EventCreate(EventBase):
    pass


class EventRead(EventBase):
    id: int
    tickets_sold: int

    	model_config = ConfigDict(from_attributes=True)
