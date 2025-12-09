from fastapi import APIRouter

from app.api.routes import predictor, health, somethings, circles, chat, intentions, actions

router = APIRouter()
router.include_router(health.router, tags=["health"], prefix="/v1")
router.include_router(predictor.router, tags=["predictor"], prefix="/v1")
router.include_router(somethings.router, tags=["somethings"], prefix="/v1/somethings")
router.include_router(circles.router, tags=["circles"], prefix="/v1/circles")
router.include_router(chat.router, tags=["chat"], prefix="/v1/chat")
router.include_router(intentions.router, tags=["intentions"], prefix="/v1/intentions")
router.include_router(actions.router, tags=["actions"], prefix="/v1/actions")
