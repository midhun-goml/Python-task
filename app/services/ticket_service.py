from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ticket import Ticket, TicketPriority, TicketStatus
from app.repositories.ticket_repositories import ticket_repository
from app.schemas.ticket_schema import TicketCreate, TicketUpdate


class TicketService:

    async def create_ticket(self, db: AsyncSession, ticket_data: TicketCreate) -> Ticket:
        current_time = datetime.now(timezone.utc)

        new_ticket = Ticket(
            title=ticket_data.title,
            description=ticket_data.description,
            priority=ticket_data.priority,
            status=TicketStatus.OPEN,
            assignee_email=ticket_data.assignee_email,
            created_at=current_time,
            updated_at=current_time
        )

        return await ticket_repository.create_ticket(db, new_ticket)

    async def get_all_tickets(
        self,
        db: AsyncSession,
        ticket_status: TicketStatus | None = None,
        priority: TicketPriority | None = None
    ) -> list[Ticket]:
        return await ticket_repository.get_all_tickets(
            db=db,
            ticket_status=ticket_status,
            priority=priority,
        )

    async def get_ticket_by_id(self, db: AsyncSession, ticket_id: UUID) -> Ticket | None:
        return await ticket_repository.get_ticket_by_id(db, ticket_id)

    async def update_ticket(
        self,
        db: AsyncSession,
        ticket_id: UUID,
        ticket_data: TicketUpdate
    ) -> Ticket | None:
        return await ticket_repository.update_ticket(db, ticket_id, ticket_data)

    async def delete_ticket(self, db: AsyncSession, ticket_id: UUID) -> bool:
        return await ticket_repository.delete_ticket(db, ticket_id)


ticket_service = TicketService()