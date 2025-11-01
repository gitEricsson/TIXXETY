import pytest
from types import SimpleNamespace
from app.services.tickets import TicketService
from app.tasks.utils import apply_expiration


class FakeEventRepo:
	def __init__(self, event):
		self._event = event
		self.incremented = 0

	async def get(self, event_id: int):
		return self._event if self._event and self._event.id == event_id else None

	async def increment_tickets_sold(self, event_id: int, inc: int = 1):
		self._event.tickets_sold += inc
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
		t = SimpleNamespace(id=tid, user_id=user_id, event_id=event_id, status="reserved")
		self._tickets[tid] = t
		return t

	async def set_status(self, ticket_id: int, status: str):
		self._tickets[ticket_id].status = status


class FakeDB:
	async def commit(self):
		return None
	async def refresh(self, _):
		return None


@pytest.mark.asyncio
async def test_sold_out_cannot_reserve(monkeypatch):
	# Event already sold out
	event = SimpleNamespace(id=1, tickets_sold=1, total_tickets=1)
	events = FakeEventRepo(event)
	tickets = FakeTicketRepo()
	db = FakeDB()

	service = TicketService(db)
	service.events = events
	service.tickets = tickets

	monkeypatch.setattr("app.tasks.tickets.schedule_ticket_expiration.delay", lambda *a, **k: None)

	with pytest.raises(Exception):
		await service.reserve_ticket(SimpleNamespace(user_id=1, event_id=1))


def test_apply_expiration_decrements_availability():
	event = SimpleNamespace(id=1, tickets_sold=1, total_tickets=1)
	ticket = SimpleNamespace(id=1, event_id=1, status="reserved")

	changed = apply_expiration(ticket, event)
	assert changed is True
	assert ticket.status == "expired"
	assert event.tickets_sold == 0


@pytest.mark.asyncio
async def test_availability_updates_allow_re_reserve_after_expiration(monkeypatch):
	# Arrange available event with one ticket
	event = SimpleNamespace(id=10, tickets_sold=0, total_tickets=1)
	events = FakeEventRepo(event)
	tickets = FakeTicketRepo()
	db = FakeDB()

	service = TicketService(db)
	service.events = events
	service.tickets = tickets

	monkeypatch.setattr("app.tasks.tickets.schedule_ticket_expiration.delay", lambda *a, **k: None)

	# First reservation succeeds and increments availability usage
	reserved = await service.reserve_ticket(SimpleNamespace(user_id=1, event_id=10))
	assert reserved.status == "reserved"
	assert event.tickets_sold == 1

	# Second reservation should fail because sold out
	with pytest.raises(Exception):
		await service.reserve_ticket(SimpleNamespace(user_id=2, event_id=10))

	# Expire the first ticket, freeing the seat
	apply_expiration(tickets._tickets[reserved.id], event)
	assert event.tickets_sold == 0

	# Now another reservation should succeed again
	reserved2 = await service.reserve_ticket(SimpleNamespace(user_id=3, event_id=10))
	assert reserved2.status == "reserved"
	assert event.tickets_sold == 1
