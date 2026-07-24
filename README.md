# AI Service Desk

An asynchronous **FastAPI-based REST API** for managing support tickets with AI-powered ticket summarization using **AWS Bedrock**. The project follows a layered architecture with SQLAlchemy Async ORM, PostgreSQL, Alembic migrations, and comprehensive unit testing.

---

## Features

- Create, Read, Update and Delete (CRUD) support tickets
- AI-powered ticket summarization using AWS Bedrock
- Async FastAPI application
- PostgreSQL database with SQLAlchemy Async ORM
- Alembic database migrations
- Pydantic request and response validation
- Response time middleware
- Health and readiness endpoints
- Unit testing using Pytest
- Performance profiling using cProfile and Pyinstrument
- Docker support

---

## Tech Stack

### Backend

- FastAPI
- Python 3.11+
- SQLAlchemy 2.0 (Async)
- PostgreSQL
- AsyncPG

### AI

- AWS Bedrock
- Jinja2 Prompt Templates

### Database

- PostgreSQL
- Alembic

### Testing

- Pytest
- Pytest-Asyncio
- FastAPI TestClient

### Performance

- cProfile
- Pyinstrument
- Locust

### Deployment

- Docker
- Uvicorn

---

## Project Structure

```text
app/
│
├── api/
│   ├── ai.py
│   └── ticket_routes.py
│
├── core/
│   ├── config.py
│   ├── database.py
│   ├── deps.py
│   └── exceptions.py
│
├── models/
│   └── ticket.py
│
├── repositories/
│   └── ticket_repositories.py
│
├── schemas/
│   └── ticket_schema.py
│
├── services/
│   ├── bedrock_service.py
│   ├── prompt_templates.py
│   └── ticket_service.py
│
├── main.py
│
tests/
│
├── test_ticket_create.py
├── test_ticket_get.py
├── test_ticket_update.py
├── test_ticket_delete.py
└── conftest.py
│
alembic/
Dockerfile
requirements.txt
README.md
```

---

## Architecture

```
                Client
                   │
                   ▼
           FastAPI Routes
                   │
                   ▼
            Service Layer
                   │
                   ▼
          Repository Layer
                   │
                   ▼
      SQLAlchemy Async ORM
                   │
                   ▼
             PostgreSQL
```

### AI Summarization Flow

```
Client
   │
   ▼
POST /ai/summarize
   │
   ▼
Bedrock Service
   │
   ▼
Jinja2 Prompt Template
   │
   ▼
AWS Bedrock
   │
   ▼
Generated Summary
```

---

# API Endpoints

## Tickets

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/tickets` | Create a ticket |
| GET | `/tickets` | Get all tickets |
| GET | `/tickets/{id}` | Get ticket by ID |
| PUT | `/tickets/{id}` | Update ticket |
| DELETE | `/tickets/{id}` | Delete ticket |

---

## AI

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/ai/summarize` | Generate ticket summary |

---

## Health Checks

| Method | Endpoint |
|---------|----------|
| GET | `/health` |
| GET | `/ready` |

---

# Ticket Schema

```json
{
    "title": "Unable to login",
    "description": "User cannot login using company credentials.",
    "priority": "high",
    "assignee_email": "agent@example.com"
}
```

---

# Validation Rules

| Field | Rule |
|--------|------|
| title | Required, max 200 characters |
| description | Optional, max 500 characters |
| priority | low, medium, high, critical |
| status | open, in_progress, resolved, closed |
| assignee_email | Valid email address |

---

# Installation

Clone the repository

```bash
git clone <repository-url>

cd ai-service-desk
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

```env
DATABASE_URL=

AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
BEDROCK_MODEL_ID=

SECRET_KEY=
ACCESS_TOKEN_EXPIRE_MINUTES=30

DEBUG=True
APP_NAME=AI Service Desk
APP_VERSION=1.0
```

---

# Database Migration

Create migration

```bash
alembic revision --autogenerate -m "Initial migration"
```

Apply migration

```bash
alembic upgrade head
```

Rollback

```bash
alembic downgrade -1
```

---

# Run the Application

```bash
uvicorn app.main:app --reload
```

Application

```
http://localhost:8000
```

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

# Running Tests

Run all tests

```bash
pytest
```

Run with coverage

```bash
pytest --cov=app
```

---

# Performance Testing

## cProfile

```bash
python profile_test.py
```

## Pyinstrument

```bash
pyinstrument app/main.py
```

## Locust

```bash
locust
```

---

# Docker

Build

```bash
docker build -t ai-service-desk .
```

Run

```bash
docker run -p 8000:8000 ai-service-desk
```

---

# Error Handling

- HTTP 422 – Validation Errors
- HTTP 404 – Ticket Not Found
- HTTP 500 – Internal Server Error

---

# Future Improvements

- JWT Authentication
- Role-Based Access Control (RBAC)
- User Management
- Email Notifications
- Pagination
- Search and Sorting
- Redis Caching
- Background Tasks
- Kubernetes Deployment
- CI/CD Pipeline

---

# Performance

Typical response times observed during development:

| Operation | Time |
|------------|------|
| Create Ticket | ~200–250 ms |
| List Tickets | ~20–50 ms |
| Get Ticket | ~5 ms |
| Update Ticket | ~15 ms |
| Delete Ticket | ~10 ms |

---

# Author

**Midhun K**

AI Service Desk Project

---
