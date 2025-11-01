import pytest
from app.services.tickets import TicketService
from types import SimpleNamespace
from datetime import datetime, timezone


class FakeEventRepo:
    def __init__(self, event):
        self._event = event
        self.incremented = 0

    async def get(self, event_id: int):
        return self._event if self._event and self._event.id == event_id else None

    async def increment_tickets_sold(self, event_id: int, inc: int = 1):
        self.incremented += inc


class FakeTicketRepo:
    def __init__(self):
        self._tickets = {}
        self._next_id = 1

    async def get(self, ticket_id: int):
        return self._tickets.get(ticket_id)

    async def create(self, user_id: int, event_id: int):
        tid = self._next_id
        self._next_id += 1
        t = SimpleNamespace(
            id=tid,
            user_id=user_id,
            event_id=event_id,
            status="reserved",
            created_at=datetime.now(timezone.utc),
        )
        self._tickets[tid] = t
        return t

    async def set_status(self, ticket_id: int, status: str):
        self._tickets[ticket_id].status = status

    async def get_by_user_id(self, user_id: int):
        return [t for t in self._tickets.values() if t.user_id == user_id]


class FakeDB:
    async def commit(self):
        return None

    async def refresh(self, obj):
        # Simulate a database setting created_at if it's not already set
        if not hasattr(obj, "created_at"):
            obj.created_at = datetime.now(timezone.utc)
        return None


@pytest.mark.asyncio
async def test_reserve_and_pay_ticket_logic(monkeypatch):
    # Arrange fakes
    fake_event = SimpleNamespace(id=1, tickets_sold=0, total_tickets=1)
    events = FakeEventRepo(fake_event)
    tickets = FakeTicketRepo()
    db = FakeDB()

    service = TicketService(db)
    service.events = events
    service.tickets = tickets

    # Stub Celery delay to no-op
    monkeypatch.setattr(
        "app.tasks.tickets.schedule_ticket_expiration.delay", lambda *a, **k: None
    )

    # Act reserve
    reserved = await service.reserve_ticket(SimpleNamespace(user_id=42, event_id=1))
    assert reserved.status == "reserved"
    assert events.incremented == 1

    # Act pay
    paid = await service.pay_ticket(reserved.id)
    assert paid.status == "paid"


@pytest.mark.asyncio
async def test_get_user_tickets():
    # Arrange fakes
    tickets = FakeTicketRepo()
    db = FakeDB()

    service = TicketService(db)
    service.tickets = tickets

    # Create some sample tickets for user 1
    await tickets.create(user_id=1, event_id=101)
    await tickets.create(user_id=1, event_id=102)
    await tickets.create(user_id=2, event_id=103)

    # Act and Assert for user 1
    user1_tickets = await service.get_user_tickets(1)
    assert len(user1_tickets) == 2
    assert all(ticket.user_id == 1 for ticket in user1_tickets)

    # Act and Assert for user 2
    user2_tickets = await service.get_user_tickets(2)
    assert len(user2_tickets) == 1
    assert all(ticket.user_id == 2 for ticket in user2_tickets)

    # Act and Assert for a user with no tickets
    user3_tickets = await service.get_user_tickets(3)
    assert len(user3_tickets) == 0
