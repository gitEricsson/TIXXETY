from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field, field_validator, ConfigDict, model_validator
from geoalchemy2.shape import to_shape


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


class EventRead(BaseModel):
    id: int
    title: str
    description: str | None = None
    start_time: datetime
    end_time: datetime
    total_tickets: int
    tickets_sold: int
    venue_address: str
    lat: float | None = None
    lng: float | None = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    def _from_model(cls, obj: Any):
        """
        If given a SQLAlchemy Event instance (has venue_location), extract fields
        and convert the geography point to lat/lng so Pydantic can validate.
        """
        # If it's already a dict (e.g. request payload), let Pydantic handle it.
        if isinstance(obj, dict):
            return obj

        # If it's a model instance with venue_location, build a dict for validation
        if hasattr(obj, "venue_location"):
            lat = lng = None
            try:
                geom = getattr(obj, "venue_location")
                if geom is not None:
                    pt = to_shape(geom)
                    lng = float(pt.x)
                    lat = float(pt.y)
            except Exception:
                # best-effort extraction; leave lat/lng as None on failure
                pass

            return {
                "id": getattr(obj, "id", None),
                "title": getattr(obj, "title", None),
                "description": getattr(obj, "description", None),
                "start_time": getattr(obj, "start_time", None),
                "end_time": getattr(obj, "end_time", None),
                "total_tickets": getattr(obj, "total_tickets", None),
                "tickets_sold": getattr(obj, "tickets_sold", None),
                "venue_address": getattr(obj, "venue_address", None),
                "lat": lat,
                "lng": lng,
            }

        return obj
