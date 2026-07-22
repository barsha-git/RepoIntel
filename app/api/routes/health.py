from fastapi import APIRouter, Depends
from app.core.config import settings

router = APIRouter(prefix="/health")

@router.get("/")
async def health_check():
    """
    Health check endpoint to verify the application is running.
    Returns a simple JSON response indicating the health status.
    """
    return {"status": "healthy", "version": settings.APP_VERSION, "environment": settings.APP_ENV}