from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.ticket import TicketPriority, TicketStatus


class TicketCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=2,
        max_length=200,
        examples=["Issue with login"]
    )

    description: str | None = Field(
        default=None,
        max_length=500,
        examples=["Users are unable to log in"]
    )

    priority: TicketPriority = Field(
        default=TicketPriority.MEDIUM,
        examples=["high"]
    )

    assignee_email: str | None = Field(
        default=None,
        max_length=256,
        examples=["agent@example.com"]
    )


class TicketUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=200
    )

    description: str | None = Field(
        default=None,
        max_length=500
    )

    priority: TicketPriority | None = None
    status: TicketStatus | None = None
    assignee_email: str | None = Field(default=None, max_length=254)


class TicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str | None
    priority: TicketPriority
    status: TicketStatus
    assignee_email: str | None
    created_at: datetime
    updated_at: datetime


class DeleteTicketResponse(BaseModel):
    message: str
    ticket_id: UUID