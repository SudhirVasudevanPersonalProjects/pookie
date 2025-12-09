"""
Health check endpoints including authentication testing.
"""
from fastapi import APIRouter, Depends
from app.core.security import get_current_user_id

router = APIRouter()


@router.get("/health")
async def health_check():
    """Basic health check endpoint (no authentication required)."""
    return {"status": "healthy"}


@router.get("/protected")
async def protected_route(user_id: str = Depends(get_current_user_id)):
    """
    Protected endpoint requiring valid JWT authentication.

    Returns authenticated user information.
    """
    return {
        "message": "Authenticated",
        "user_id": user_id
    }
