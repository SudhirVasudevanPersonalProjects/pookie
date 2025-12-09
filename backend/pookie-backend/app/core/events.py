from typing import Callable

from fastapi import FastAPI
from app.services.embedding_service import embedding_service
from app.services.vector_service import vector_service
from loguru import logger


def preload_model():
    """
    In order to load model on memory to each worker
    """
    try:
        from app.services.predict import MachineLearningModelHandlerScore
        MachineLearningModelHandlerScore.get_model()
    except ImportError:
        # Prediction service not yet implemented, skip preload
        logger.debug("Prediction service not available, skipping preload")


async def on_startup():
    """FastAPI startup event handler"""
    logger.info("Application startup - loading ML models and indices")

    # Load existing prediction models (disabled due to implementation issues)
    # preload_model()

    # Load embedding model into memory
    embedding_service.load_model()

    # Load FAISS index from Supabase Storage
    await vector_service.initialize()

    logger.info("Startup complete - all services ready")


async def on_shutdown():
    """FastAPI shutdown event handler"""
    logger.info("Application shutdown")


def create_start_app_handler(app: FastAPI) -> Callable:
    def start_app() -> None:
        preload_model()

    return start_app
