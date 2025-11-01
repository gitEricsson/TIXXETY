import pytest
from app.services.tickets import TicketService
from types import SimpleNamespace


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
	monkeypatch.setattr("app.tasks.tickets.schedule_ticket_expiration.delay", lambda *a, **k: None)

	# Act reserve
	reserved = await service.reserve_ticket(SimpleNamespace(user_id=42, event_id=1))
	assert reserved.status == "reserved"
	assert events.incremented == 1

	# Act pay
	paid = await service.pay_ticket(reserved.id)
	assert paid.status == "paid"
