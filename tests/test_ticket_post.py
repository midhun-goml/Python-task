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


# ---------------------------------------------------------
# create_ticket
# ---------------------------------------------------------



@pytest.mark.asyncio
async def test_create_ticket_sets_status_open(db, monkeypatch):
    # HAPPY
    repo_mock = AsyncMock(return_value=make_ticket())

    monkeypatch.setattr(ticket_repository, "create_ticket", repo_mock)

    await ticket_service.create_ticket(
        db,
        TicketCreate(title="Login Issue"),
    )

    _, ticket = repo_mock.await_args.args

    assert ticket.status == TicketStatus.OPEN


@pytest.mark.asyncio
async def test_create_ticket_copies_title(db, monkeypatch):
    # HAPPY
    repo_mock = AsyncMock(return_value=make_ticket())

    monkeypatch.setattr(ticket_repository, "create_ticket", repo_mock)

    payload = TicketCreate(title="Server Down")

    await ticket_service.create_ticket(db, payload)

    _, ticket = repo_mock.await_args.args

    assert ticket.title == payload.title


@pytest.mark.asyncio
async def test_create_ticket_copies_description(db, monkeypatch):
    # HAPPY
    repo_mock = AsyncMock(return_value=make_ticket())

    monkeypatch.setattr(ticket_repository, "create_ticket", repo_mock)

    payload = TicketCreate(
        title="Issue",
        description="API is unavailable",
    )

    await ticket_service.create_ticket(db, payload)

    _, ticket = repo_mock.await_args.args

    assert ticket.description == payload.description


@pytest.mark.asyncio
async def test_create_ticket_copies_priority(db, monkeypatch):
    # HAPPY
    repo_mock = AsyncMock(return_value=make_ticket())

    monkeypatch.setattr(ticket_repository, "create_ticket", repo_mock)

    payload = TicketCreate(
        title="Issue",
        priority=TicketPriority.HIGH,
    )

    await ticket_service.create_ticket(db, payload)

    _, ticket = repo_mock.await_args.args

    assert ticket.priority == TicketPriority.HIGH


@pytest.mark.asyncio
async def test_create_ticket_copies_assignee_email(db, monkeypatch):
    # HAPPY
    repo_mock = AsyncMock(return_value=make_ticket())

    monkeypatch.setattr(ticket_repository, "create_ticket", repo_mock)

    payload = TicketCreate(
        title="Issue",
        assignee_email="midhun@test1.com",
    )

    await ticket_service.create_ticket(db, payload)

    _, ticket = repo_mock.await_args.args

    assert ticket.assignee_email == payload.assignee_email


# ---------------------------------------------------------
# get_all_tickets
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_get_all_tickets_returns_repository_result(db, monkeypatch):
    # HAPPY
    expected = [make_ticket()]

    repo_mock = AsyncMock(return_value=expected)

    monkeypatch.setattr(ticket_repository, "get_all_tickets", repo_mock)

    result = await ticket_service.get_all_tickets(db)

    assert result == expected


# ---------------------------------------------------------
# get_ticket_by_id
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# update_ticket
# ---------------------------------------------------------

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



# ---------------------------------------------------------
# delete_ticket
# ---------------------------------------------------------

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
