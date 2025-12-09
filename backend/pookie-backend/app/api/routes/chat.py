"""
Chat API endpoints with SSE streaming.
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from loguru import logger

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.schemas.chat import ChatQueryRequest
from app.services.chat_service import chat_service
import json


router = APIRouter()


@router.post("/stream")
async def stream_chat(
    request: ChatQueryRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Stream chat response with personalized RAG context.

    **Authentication:** Requires JWT token

    **Request Body:**
    - query (str): User's question (1-500 characters)
    - top_k (int, optional): Number of somethings to retrieve (1-50, default: 10)

    **Response:** Server-Sent Events (SSE) stream
    - Content-Type: text/event-stream
    - Events: `data: {"token": "..."}\n\n` for each token
    - Final event: `data: {"done": true, "circles_used": [...]}\n\n`
    - Error event: `data: {"error": "..."}\n\n`

    **Example:**
    ```
    data: {"token": "Based"}
    data: {"token": " on"}
    data: {"token": " your"}
    data: {"token": " Fitness"}
    data: {"token": " circle..."}
    data: {"done": true, "circles_used": ["Fitness", "Career"]}
    ```
    """

    async def event_generator():
        """Generate SSE events from chat service."""
        try:
            async for event in chat_service.stream_chat(
                query=request.query,
                user_id=user_id,
                db=db,
                top_k=request.top_k
            ):
                # Format as SSE: data: {json}\n\n
                yield f"data: {json.dumps(event)}\n\n"

        except Exception as e:
            logger.error(f"Chat stream error: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )
