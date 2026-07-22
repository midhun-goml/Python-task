from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.core.exceptions import TicketNotFoundError
from app.models.ticket import TicketPriority, TicketStatus
from app.schemas.ticket_schema import (
    DeleteTicketResponse,
    TicketCreate,
    TicketResponse,
    TicketUpdate
)
from app.services.ticket_service import ticket_service


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


@router.post(
    "",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_ticket(
    ticket_data: TicketCreate,
    db: AsyncSession = Depends(get_db)
):
    return await ticket_service.create_ticket(db, ticket_data)


@router.get(
    "",
    response_model=list[TicketResponse]
)
async def get_all_tickets(
    ticket_status: TicketStatus | None = Query(
        default=None,
        alias="status"
    ),
    priority: TicketPriority | None = Query(default=None),
    db: AsyncSession = Depends(get_db)
):
    return await ticket_service.get_all_tickets(
        db=db,
        ticket_status=ticket_status,
        priority=priority
    )


@router.get(
    "/{ticket_id}",
    response_model=TicketResponse
)
async def get_ticket_by_id(
    ticket_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    ticket = await ticket_service.get_ticket_by_id(db, ticket_id)

    if ticket is None:
        raise TicketNotFoundError(str(ticket_id))

    return ticket


@router.put(
    "/{ticket_id}",
    response_model=TicketResponse
)
async def update_ticket(
    ticket_id: UUID,
    ticket_data: TicketUpdate,
    db: AsyncSession = Depends(get_db)
):
    updated_ticket = await ticket_service.update_ticket(db, ticket_id, ticket_data)

    if updated_ticket is None:
        raise TicketNotFoundError(str(ticket_id))

    return updated_ticket


@router.delete(
    "/{ticket_id}",
    response_model=DeleteTicketResponse
)
async def delete_ticket(
    ticket_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    deleted = await ticket_service.delete_ticket(db, ticket_id)

    if not deleted:
        raise TicketNotFoundError(str(ticket_id))

    return DeleteTicketResponse(
        message="Ticket deleted successfully",
        ticket_id=ticket_id
    )