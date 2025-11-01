import asyncio
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_engine, Base, AsyncSessionLocal
from app.models.user import User
from app.models.event import Event
from app.models.ticket import Ticket
from app.core.config import settings


async def seed_db():
    print("Seeding database...")

    # Drop all tables and recreate them
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        # Create users
        user1 = User(name="Alice Smith", email="alice@example.com")
        user2 = User(name="Bob Johnson", email="bob@example.com")
        user3 = User(name="Charlie Brown", email="charlie@example.com")
        session.add_all([user1, user2, user3])
        await session.flush()  # Flush to get IDs

        # Create events
        event1 = Event(
            title="Concert in the Park",
            description="A lovely evening of music.",
            total_tickets=100,
            tickets_sold=0,
            date=datetime.utcnow() + timedelta(days=7),
            location="Central Park",
        )
        event2 = Event(
            title="Tech Conference 2024",
            description="The latest in technology.",
            total_tickets=50,
            tickets_sold=0,
            date=datetime.utcnow() + timedelta(days=30),
            location="Convention Center",
        )
        event3 = Event(
            title="Art Exhibition",
            description="Showcasing local artists.",
            total_tickets=20,
            tickets_sold=0,
            date=datetime.utcnow() + timedelta(days=15),
            location="Art Gallery",
        )
        session.add_all([event1, event2, event3])
        await session.flush()  # Flush to get IDs

        # Create tickets
        # User 1 tickets
        ticket1_1 = Ticket(user_id=user1.id, event_id=event1.id, status="reserved")
        ticket1_2 = Ticket(user_id=user1.id, event_id=event1.id, status="paid")
        ticket1_3 = Ticket(user_id=user1.id, event_id=event2.id, status="reserved")

        # User 2 tickets
        ticket2_1 = Ticket(user_id=user2.id, event_id=event1.id, status="paid")
        ticket2_2 = Ticket(user_id=user2.id, event_id=event3.id, status="reserved")

        # User 3 no tickets (for testing empty history)

        session.add_all([ticket1_1, ticket1_2, ticket1_3, ticket2_1, ticket2_2])

        # Update tickets_sold for events
        event1.tickets_sold += 3  # ticket1_1, ticket1_2, ticket2_1
        event2.tickets_sold += 1  # ticket1_3
        event3.tickets_sold += 1  # ticket2_2

        await session.commit()
        print("Database seeding complete.")


if __name__ == "__main__":
    asyncio.run(seed_db())
