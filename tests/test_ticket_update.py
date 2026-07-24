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
async def test_update_ticket_returns_repository_result(db, monkeypatch):
    # HAPPY
    expected = make_ticket()

    repo_mock = AsyncMock(return_value=expected)

    monkeypatch.setattr(ticket_repository, "update_ticket", repo_mock)

    result = await ticket_service.update_ticket(
        db,
        uuid4(),
        TicketUpdate(status=TicketStatus.RESOLVED),
    )

    assert result.status == expected.status

@pytest.mark.asyncio
async def test_update_ticket_passes_correct_ticket_id(db, monkeypatch):
    repo_mock = AsyncMock(return_value=make_ticket())

    monkeypatch.setattr(ticket_repository, "update_ticket", repo_mock)

    ticket_id = uuid4()
    payload = TicketUpdate(title="Updated")

    await ticket_service.update_ticket(db, ticket_id, payload)

    _, passed_id, _ = repo_mock.await_args.args

    assert passed_id == ticket_id

@pytest.mark.asyncio
async def test_update_ticket_returns_updated_title(db, monkeypatch):
    expected = make_ticket(title="Updated")

    repo_mock = AsyncMock(return_value=expected)

    monkeypatch.setattr(ticket_repository, "update_ticket", repo_mock)

    result = await ticket_service.update_ticket(
        db,
        expected.id,
        TicketUpdate(title="Updated"),
    )

    assert result.title == "Updated"

@pytest.mark.asyncio
async def test_update_ticket_returns_updated_priority(db, monkeypatch):
    expected = make_ticket(priority=TicketPriority.HIGH)

    repo_mock = AsyncMock(return_value=expected)

    monkeypatch.setattr(ticket_repository, "update_ticket", repo_mock)

    result = await ticket_service.update_ticket(
        db,
        expected.id,
        TicketUpdate(priority=TicketPriority.HIGH),
    )

    assert result.priority == TicketPriority.HIGH

@pytest.mark.asyncio
async def test_update_ticket_returns_updated_assignee_email(db, monkeypatch):
    expected = make_ticket(assignee_email="newagent@test.com")

    repo_mock = AsyncMock(return_value=expected)

    monkeypatch.setattr(ticket_repository, "update_ticket", repo_mock)

    result = await ticket_service.update_ticket(
        db,
        expected.id,
        TicketUpdate(assignee_email="newagent@test.com"),
    )

    assert result.assignee_email == "newagent@test.com"

@pytest.mark.asyncio
async def test_update_ticket_accepts_partial_update(db, monkeypatch):
    repo_mock = AsyncMock(return_value=make_ticket())

    monkeypatch.setattr(ticket_repository, "update_ticket", repo_mock)

    payload = TicketUpdate(status=TicketStatus.IN_PROGRESS)

    await ticket_service.update_ticket(db, uuid4(), payload)

    _, _, passed_payload = repo_mock.await_args.args

    assert passed_payload.status == TicketStatus.IN_PROGRESS
    assert passed_payload.title is None


@pytest.mark.asyncio
async def test_update_ticket_returns_none(db, monkeypatch):
    # FAILURE
    repo_mock = AsyncMock(return_value=None)

    monkeypatch.setattr(ticket_repository, "update_ticket", repo_mock)

    result = await ticket_service.update_ticket(
        db,
        uuid4(),
        TicketUpdate(title="Updated"),
    )

    assert result is None
