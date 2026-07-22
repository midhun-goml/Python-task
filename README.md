# AI Service Desk

## What was implemented

The app now uses PostgreSQL through SQLAlchemy async sessions, Alembic is bootstrapped, ticket responses can serialize ORM objects, and the API exposes health/readiness checks plus custom ticket-not-found handling.

## Step-by-step implementation

1. Define the database base.
   - Create [app/models/base.py](app/models/base.py) with `DeclarativeBase`.
   - Make every ORM model inherit from `Base`.

2. Convert the ticket model to SQLAlchemy.
   - Update [app/models/ticket.py](app/models/ticket.py).
   - Keep `TicketPriority` and `TicketStatus` as restricted enums.
   - Map the table name to `tickets`.
   - Add `id`, `title`, `description`, `priority`, `status`, `assignee_email`, `created_at`, and `updated_at`.

3. Add PostgreSQL configuration.
   - Update [app/core/config.py](app/core/config.py) so `DATABASE_URL` points to PostgreSQL with `postgresql+asyncpg://...`.
   - Set the same URL in [.env](.env) for local runs.

4. Add async database helpers.
   - Create [app/core/database.py](app/core/database.py) with `create_async_engine` and `AsyncSessionLocal`.
   - Create [app/core/deps.py](app/core/deps.py) with `get_db()`.
   - Commit after the request succeeds, roll back on exception, and always close the session.

5. Add a custom domain exception.
   - Create [app/core/exceptions.py](app/core/exceptions.py).
   - Store the missing `ticket_id` as a string in `TicketNotFoundError`.

6. Update schemas for ORM response mapping.
   - Update [app/schemas/ticket_schema.py](app/schemas/ticket_schema.py).
   - Add `assignee_email` to create and update schemas.
   - Add `model_config = ConfigDict(from_attributes=True)` to `TicketResponse`.

7. Move ticket CRUD to PostgreSQL.
   - Refactor [app/services/ticket_service.py](app/services/ticket_service.py) to use `AsyncSession`.
   - Replace the in-memory dictionary with SQLAlchemy CRUD calls.
   - Use `db.add`, `db.get`, `select`, `db.delete`, `flush`, and `refresh`.

8. Wire the routes to database sessions.
   - Update [app/api/ticket_routes.py](app/api/ticket_routes.py).
   - Add `Depends(get_db)` to the ticket routes.
   - Raise `TicketNotFoundError` instead of `HTTPException`.

9. Add middleware and system endpoints.
   - Update [app/main.py](app/main.py).
   - Record time before `call_next()`.
   - Set `X-Response-Time` on every response.
   - Add `GET /health` for liveness.
   - Add `GET /ready` for database readiness using `SELECT 1`.

10. Bootstrap Alembic.
    - Add [alembic.ini](alembic.ini).
    - Add [alembic/env.py](alembic/env.py).
    - Add [alembic/script.py.mako](alembic/script.py.mako).
    - Add the revision [alembic/versions/0001_add_assignee_email.py](alembic/versions/0001_add_assignee_email.py).

## Expected commands

```powershell
e:/GoML/Python_HandsOn/ai-service-desk/.venv/Scripts/python.exe -c "from app.models.ticket import Ticket; print(Ticket.__tablename__)"
alembic revision --autogenerate -m "add_assignee_email"
alembic upgrade head
alembic downgrade -1
alembic upgrade head
uvicorn app.main:app --reload
```

## Migration note

If `status` were renamed to `ticket_status` instead of adding `assignee_email`, Alembic would usually interpret that as a drop plus add, not a rename. The safe manual fix would be to edit the revision to perform a rename or a batch table alteration, depending on the database backend.

## Health and readiness

- `GET /health` is the fast liveness route.
- `GET /ready` checks PostgreSQL connectivity.

## Response timing

- Every response now includes `X-Response-Time`.
