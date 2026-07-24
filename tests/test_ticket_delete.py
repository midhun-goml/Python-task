from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.models.ticket import TicketPriority, TicketStatus
from app.repositories.ticket_repositories import ticket_repository
from app.schemas.ticket_schema import TicketCreate, TicketUpdate
from app.services.ticket_service import ticket_service


@pytest.fixture
def db():
    return object()


def make_ticket():
    return SimpleNamespace(
        id=uuid4(),
        title="Login Issue",
        description="Unable to login",
        priority=TicketPriority.MEDIUM,
        status=TicketStatus.OPEN,
        assignee_email="agent@example.com",
    )

@pytest.mark.asyncio
async def test_delete_ticket_returns_true(db, monkeypatch):
    # HAPPY
    repo_mock = AsyncMock(return_value=True)

    monkeypatch.setattr(ticket_repository, "delete_ticket", repo_mock)

    result = await ticket_service.delete_ticket(db, uuid4())

    assert result is True


@pytest.mark.asyncio
async def test_delete_ticket_returns_false(db, monkeypatch):
    # FAILURE
    repo_mock = AsyncMock(return_value=False)

    monkeypatch.setattr(ticket_repository, "delete_ticket", repo_mock)

    result = await ticket_service.delete_ticket(db, uuid4())

    assert result is False

@pytest.mark.asyncio
async def test_delete_ticket_passes_correct_ticket_id(db, monkeypatch):
    repo_mock = AsyncMock(return_value=True)

    monkeypatch.setattr(ticket_repository, "delete_ticket", repo_mock)

    ticket_id = uuid4()

    await ticket_service.delete_ticket(db, ticket_id)

    _, passed_id = repo_mock.await_args.args

    assert passed_id == ticket_id


@pytest.mark.asyncio
async def test_delete_ticket_returns_none(db, monkeypatch):
    repo_mock = AsyncMock(return_value=None)

    monkeypatch.setattr(ticket_repository, "delete_ticket", repo_mock)

    result = await ticket_service.delete_ticket(db, uuid4())

    assert result is None

