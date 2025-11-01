from datetime import datetime
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text
from geoalchemy2 import Geography
from app.db.session import Base


class Event(Base):
	__tablename__ = "events"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	title: Mapped[str] = mapped_column(String(200), nullable=False)
	description: Mapped[str | None] = mapped_column(String(2000), nullable=True)
	start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
	end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
	total_tickets: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
	tickets_sold: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
	venue_address: Mapped[str] = mapped_column(String(400), nullable=False)
	# PostGIS geography Point (lon/lat)
	venue_location = mapped_column(Geography(geometry_type="POINT", srid=4326, spatial_index=True), nullable=False)
