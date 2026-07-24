from time import perf_counter

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.api.ai import router as ai_router
from app.api.ticket_routes import router as ticket_router
from app.core.config import settings
from app.core.database import engine
from app.core.exceptions import TicketNotFoundError
from app.models.base import Base

from fastapi.middleware.cors import CORSMiddleware
from pyinstrument import Profiler

import cProfile
import io
import pstats

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    description="Ticket CRUD API for AI Service Desk"
)


app.include_router(ticket_router)
app.include_router(ai_router)

@app.middleware("http")
async def add_response_time_header(request: Request, call_next):
    start_time = perf_counter()
    response = await call_next(request)
    elapsed_ms = (perf_counter() - start_time) * 1000
    response.headers["X-Response-Time"] = f"{elapsed_ms:.0f}ms"
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(TicketNotFoundError)
async def ticket_not_found_handler(_: Request, exc: TicketNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"error": "ticket_not_found", "id": exc.ticket_id}
    )


@app.get("/", tags=["Root"])
def home():
    return {
        "message": f"{settings.APP_NAME} is running",
        "version": settings.APP_VERSION,
        "documentation": "/docs"
    }


@app.get("/health", tags=["System"])
async def health():
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))
    return {"status": "ok + database connection successful"}


@app.get("/ready", tags=["System"])
async def ready():
    return {"status": "ready"}
