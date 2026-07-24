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


def test_make_ticket_returns_ticket():
    ticket = make_ticket()

    assert ticket is not None

def test_make_ticket_generates_unique_ids():
    ticket1 = make_ticket()
    ticket2 = make_ticket()

    assert ticket1.id != ticket2.id

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

@pytest.mark.asyncio
async def test_create_ticket_description_defaults_to_none(db, monkeypatch):
    repo_mock = AsyncMock(return_value=make_ticket())

    monkeypatch.setattr(ticket_repository, "create_ticket", repo_mock)

    await ticket_service.create_ticket(
        db,
        TicketCreate(title="Issue"),
    )

    _, ticket = repo_mock.await_args.args

    assert ticket.description is None

@pytest.mark.asyncio
async def test_create_ticket_default_priority_is_low(db, monkeypatch):
    repo_mock = AsyncMock(return_value=make_ticket())

    monkeypatch.setattr(ticket_repository, "create_ticket", repo_mock)

    await ticket_service.create_ticket(
        db,
        TicketCreate(title="Issue"),
    )

    _, ticket = repo_mock.await_args.args

    assert ticket.priority == TicketPriority.MEDIUM

@pytest.mark.asyncio
async def test_create_ticket_accepts_max_length_title(db, monkeypatch):
    repo_mock = AsyncMock(return_value=make_ticket())

    monkeypatch.setattr(ticket_repository, "create_ticket", repo_mock)

    title = "A" * 200

    await ticket_service.create_ticket(
        db,
        TicketCreate(title=title),
    )

    _, ticket = repo_mock.await_args.args

    assert ticket.title == title

@pytest.mark.asyncio
async def test_create_ticket_does_not_assign_ticket_id(db, monkeypatch):
    repo_mock = AsyncMock(return_value=make_ticket())

    monkeypatch.setattr(ticket_repository, "create_ticket", repo_mock)

    await ticket_service.create_ticket(
        db,
        TicketCreate(title="Issue"),
    )

    _, ticket = repo_mock.await_args.args

    assert ticket.id is None
