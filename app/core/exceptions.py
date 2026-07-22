class TicketNotFoundError(Exception):
    def __init__(self, ticket_id: str) -> None:
        self.ticket_id = ticket_id
        super().__init__(f"Ticket {ticket_id} was not found")