from fastapi import FastAPI

from app.api.ticket_routes import router as ticket_router
from app.core.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    description="Ticket CRUD API for AI Service Desk"
)


app.include_router(ticket_router)


@app.get("/", tags=["Root"])
def home():
    return {
        "message": f"{settings.APP_NAME} is running",
        "version": settings.APP_VERSION,
        "documentation": "/docs"
    }
