from fastapi import APIRouter

from app.api.routes import predictor, health, somethings

router = APIRouter()
router.include_router(health.router, tags=["health"], prefix="/v1")
router.include_router(predictor.router, tags=["predictor"], prefix="/v1")
router.include_router(somethings.router, tags=["somethings"], prefix="/v1/somethings")
