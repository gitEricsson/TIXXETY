def apply_expiration(ticket, event):
	if ticket.status != "reserved":
		return False
	ticket.status = "expired"
	if event and getattr(event, "tickets_sold", 0) > 0:
		event.tickets_sold -= 1
	return True
