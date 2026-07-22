from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ticket import Ticket, TicketPriority, TicketStatus
from app.schemas.ticket_schema import TicketUpdate


class TicketRepository:

	async def create_ticket(self, db: AsyncSession, ticket: Ticket) -> Ticket:
		db.add(ticket)
		await db.flush()
		await db.refresh(ticket)
		return ticket

	async def get_all_tickets(
		self,
		db: AsyncSession,
		ticket_status: TicketStatus | None = None,
		priority: TicketPriority | None = None,
	) -> list[Ticket]:
		query = select(Ticket)

		if ticket_status is not None:
			query = query.where(Ticket.status == ticket_status)

		if priority is not None:
			query = query.where(Ticket.priority == priority)

		result = await db.execute(query)
		return list(result.scalars().all())

	async def get_ticket_by_id(self, db: AsyncSession, ticket_id: UUID) -> Ticket | None:
		return await db.get(Ticket, ticket_id)

	async def update_ticket(
		self,
		db: AsyncSession,
		ticket_id: UUID,
		ticket_data: TicketUpdate,
	) -> Ticket | None:
		existing_ticket = await db.get(Ticket, ticket_id)

		if existing_ticket is None:
			return None

		update_values = ticket_data.model_dump(exclude_unset=True)

		for field_name, field_value in update_values.items():
			setattr(existing_ticket, field_name, field_value)

		await db.flush()
		await db.refresh(existing_ticket)
		return existing_ticket

	async def delete_ticket(self, db: AsyncSession, ticket_id: UUID) -> bool:
		existing_ticket = await db.get(Ticket, ticket_id)

		if existing_ticket is None:
			return False

		await db.delete(existing_ticket)
		await db.flush()
		return True


ticket_repository = TicketRepository()
