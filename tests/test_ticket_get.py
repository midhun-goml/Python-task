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

#get all tickets :

@pytest.mark.asyncio
async def test_get_all_tickets_returns_repository_result(db, monkeypatch):
    # HAPPY
    expected = [make_ticket()]

    repo_mock = AsyncMock(return_value=expected)

    monkeypatch.setattr(ticket_repository, "get_all_tickets", repo_mock)

    result = await ticket_service.get_all_tickets(db)

    assert result == expected

@pytest.mark.asyncio
async def test_get_all_tickets_returns_empty_list(db, monkeypatch):
    repo_mock = AsyncMock(return_value=[])

    monkeypatch.setattr(ticket_repository, "get_all_tickets", repo_mock)

    result = await ticket_service.get_all_tickets(db)

    assert result == []

@pytest.mark.asyncio
async def test_get_all_tickets_returns_multiple_tickets(db, monkeypatch):
    expected = [
        make_ticket(),
        make_ticket(),
        make_ticket(),
    ]

    repo_mock = AsyncMock(return_value=expected)

    monkeypatch.setattr(ticket_repository, "get_all_tickets", repo_mock)

    result = await ticket_service.get_all_tickets(db)

    assert len(result) == 3
    assert result == expected

@pytest.mark.asyncio
async def test_get_all_tickets_returns_list(db, monkeypatch):
    repo_mock = AsyncMock(return_value=[make_ticket()])

    monkeypatch.setattr(ticket_repository, "get_all_tickets", repo_mock)

    result = await ticket_service.get_all_tickets(db)

    assert isinstance(result, list)

@pytest.mark.asyncio
async def test_get_all_tickets_preserves_ticket_data(db, monkeypatch):
    expected = [
        make_ticket(),
        make_ticket(),
    ]

    repo_mock = AsyncMock(return_value=expected)

    monkeypatch.setattr(ticket_repository, "get_all_tickets", repo_mock)

    result = await ticket_service.get_all_tickets(db)

    for actual, expected_ticket in zip(result, expected):
        assert actual.title == expected_ticket.title
        assert actual.priority == expected_ticket.priority
        assert actual.status == expected_ticket.status

#get ticket by id :

@pytest.mark.asyncio
async def test_get_ticket_by_id_returns_correct_title(db, monkeypatch):
    # HAPPY
    expected = make_ticket()

    repo_mock = AsyncMock(return_value=expected)
    monkeypatch.setattr(ticket_repository, "get_ticket_by_id", repo_mock)

    result = await ticket_service.get_ticket_by_id(db, expected.id)

    assert result.title == expected.title


@pytest.mark.asyncio
async def test_get_ticket_by_id_returns_none(db, monkeypatch):
    # FAILURE
    repo_mock = AsyncMock(return_value=None)

    monkeypatch.setattr(ticket_repository, "get_ticket_by_id", repo_mock)

    result = await ticket_service.get_ticket_by_id(db, uuid4())

    assert result is None

@pytest.mark.asyncio
async def test_get_ticket_by_id_returns_correct_id(db, monkeypatch):
    expected = make_ticket()

    repo_mock = AsyncMock(return_value=expected)

    monkeypatch.setattr(ticket_repository, "get_ticket_by_id", repo_mock)

    result = await ticket_service.get_ticket_by_id(db, expected.id)

    assert result.id == expected.id

@pytest.mark.asyncio
async def test_get_ticket_by_id_returns_correct_status(db, monkeypatch):
    expected = make_ticket()

    repo_mock = AsyncMock(return_value=expected)

    monkeypatch.setattr(ticket_repository, "get_ticket_by_id", repo_mock)

    result = await ticket_service.get_ticket_by_id(db, expected.id)

    assert result.status == TicketStatus.OPEN

@pytest.mark.asyncio
async def test_get_ticket_by_id_returns_correct_priority(db, monkeypatch):
    expected = make_ticket()

    repo_mock = AsyncMock(return_value=expected)

    monkeypatch.setattr(ticket_repository, "get_ticket_by_id", repo_mock)

    result = await ticket_service.get_ticket_by_id(db, expected.id)

    assert result.priority == TicketPriority.MEDIUM

@pytest.mark.asyncio
async def test_get_ticket_by_id_returns_correct_assignee_email(db, monkeypatch):
    expected = make_ticket()

    repo_mock = AsyncMock(return_value=expected)

    monkeypatch.setattr(ticket_repository, "get_ticket_by_id", repo_mock)

    result = await ticket_service.get_ticket_by_id(db, expected.id)

    assert result.assignee_email == expected.assignee_email
