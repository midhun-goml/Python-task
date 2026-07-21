from fastapi import APIRouter

from app.api.ticket_routes import router as tickets_router

router = APIRouter()
router.include_router(tickets_router)

__all__ = ["router"]