"""Somethings CRUD API endpoints.

Story 2.4: Provides RESTful API for creating, reading, updating, and deleting somethings
with automatic embedding generation and meaning generation.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.something import Something
from app.schemas.something import SomethingCreate, SomethingResponse, SomethingUpdateMeaning, CirclePrediction
from app.services.embedding_service import embedding_service
from app.services.vector_service import vector_service
from app.services.llm_service import llm_service
from app.services.centroid_service import centroid_service
from loguru import logger

router = APIRouter()


@router.post(
    "",
    response_model=SomethingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new something",
    description="Create a new something with automatic embedding generation and meaning generation for text content"
)
async def create_something(
    something_data: SomethingCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Create new something with automatic embedding and meaning generation.

    **Process:**
    1. Create something in database
    2. Generate embedding from content
    3. Add embedding to FAISS index
    4. Generate meaning (text content only, async)
    5. Save FAISS index every 10 somethings (debounced)

    **Returns:**
    - 201 Created with SomethingResponse
    """
    try:
        # Convert user_id string to UUID
        user_uuid = UUID(user_id)

        # Create something in database
        db_something = Something(
            user_id=user_uuid,
            content=something_data.content,
            content_type=something_data.content_type.value,
            media_url=something_data.media_url
        )
        db.add(db_something)
        db.commit()
        db.refresh(db_something)

        logger.info(f"Created something {db_something.id} for user {user_id}")

        # Generate embedding from text content only
        # Note: Media URLs are not embedded - only actual text content
        # Future: For images/videos, use multimodal embeddings (Epic 3+)
        if something_data.content and something_data.content.strip():
            embedding = embedding_service.generate_embedding(something_data.content)

            # Add to FAISS index
            await vector_service.add_something_embedding(
                something_id=db_something.id,
                embedding=embedding
            )

            logger.info(f"Generated embedding and added to FAISS index for something {db_something.id}")
        else:
            logger.debug(f"Something {db_something.id} has no text content for embedding (media-only or empty)")

        # Generate meaning for text content only (async)
        if something_data.content and something_data.content_type.value == "text":
            meaning = llm_service.generate_meaning(something_data.content)
            if meaning:
                db_something.meaning = meaning
                db.commit()
                db.refresh(db_something)
                logger.info(f"Generated meaning for something {db_something.id}")
            else:
                logger.debug(f"LLM service returned None for something {db_something.id} (stub mode or failure)")

        # Debounced FAISS save every 10 somethings
        # Use something ID modulo to avoid expensive count query
        if db_something.id % 10 == 0:
            await vector_service.save_to_storage()
            logger.info(f"FAISS index saved at something ID: {db_something.id}")

        # Predict circle suggestions using centroid similarity (MVP-1)
        # This helps users organize their thoughts with AI assistance
        suggested_circles = []
        try:
            predictions = centroid_service.predict_circles_for_something(
                something_id=db_something.id,
                user_id=user_id,
                db=db,
                threshold=0.7,
                top_k=3
            )
            suggested_circles = [
                CirclePrediction(**p)  # Unpack dict directly since keys match field names
                for p in predictions
            ]
            logger.info(f"Predicted {len(suggested_circles)} circles for something {db_something.id}")
        except Exception as e:
            # Graceful degradation - don't fail creation if prediction fails
            logger.warning(f"Circle prediction failed for something {db_something.id}: {str(e)}")

        # Build response with suggestions using model_validate
        # serialization_alias in the schema handles snake_case to camelCase output
        response = SomethingResponse.model_validate(db_something)
        response.suggested_circles = suggested_circles
        
        return response

    except ValueError as e:
        logger.error(f"Invalid UUID format: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid user ID format: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create something: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create something"
        )


@router.get(
    "",
    response_model=List[SomethingResponse],
    summary="List user's somethings",
    description="Get paginated list of user's somethings, sorted by created_at descending"
)
async def list_somethings(
    skip: int = 0,
    limit: int = 100,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    List user's somethings with pagination.

    **Query Parameters:**
    - skip: Number of records to skip (default: 0)
    - limit: Maximum number of records to return (default: 100)

    **Returns:**
    - List of SomethingResponse objects, sorted by created_at descending
    """
    try:
        user_uuid = UUID(user_id)

        somethings = (
            db.query(Something)
            .filter(Something.user_id == user_uuid)
            .order_by(Something.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        logger.info(f"Retrieved {len(somethings)} somethings for user {user_id} (skip={skip}, limit={limit})")

        return [SomethingResponse.model_validate(s) for s in somethings]

    except ValueError as e:
        logger.error(f"Invalid UUID format: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid user ID format: {str(e)}"
        )


@router.get(
    "/{something_id}",
    response_model=SomethingResponse,
    summary="Get single something",
    description="Retrieve a specific something by ID (with ownership validation)"
)
async def get_something(
    something_id: int,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get single something by ID with ownership validation.

    **Returns:**
    - 200 OK with SomethingResponse
    - 404 Not Found if something doesn't exist or doesn't belong to user
    """
    try:
        user_uuid = UUID(user_id)

        something = (
            db.query(Something)
            .filter(
                Something.id == something_id,
                Something.user_id == user_uuid
            )
            .first()
        )

        if not something:
            logger.warning(f"Something {something_id} not found for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Something with id {something_id} not found"
            )

        logger.info(f"Retrieved something {something_id} for user {user_id}")

        return SomethingResponse.model_validate(something)

    except ValueError as e:
        logger.error(f"Invalid UUID format: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid user ID format: {str(e)}"
        )


@router.patch(
    "/{something_id}/meaning",
    response_model=SomethingResponse,
    summary="Update something meaning",
    description="Update meaning field (user edit as learning signal)"
)
async def update_something_meaning(
    something_id: int,
    meaning_update: SomethingUpdateMeaning,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Update meaning field for a something.

    Sets is_meaning_user_edited = True to signal LLM learning.

    **Returns:**
    - 200 OK with updated SomethingResponse
    - 404 Not Found if something doesn't exist or doesn't belong to user
    """
    try:
        user_uuid = UUID(user_id)

        something = (
            db.query(Something)
            .filter(
                Something.id == something_id,
                Something.user_id == user_uuid
            )
            .first()
        )

        if not something:
            logger.warning(f"Something {something_id} not found for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Something with id {something_id} not found"
            )

        # Update meaning and mark as user-edited
        something.meaning = meaning_update.meaning
        something.is_meaning_user_edited = True

        db.commit()
        db.refresh(something)

        logger.info(f"Updated meaning for something {something_id} (user edit)")

        return SomethingResponse.model_validate(something)

    except ValueError as e:
        logger.error(f"Invalid UUID format: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid user ID format: {str(e)}"
        )


@router.delete(
    "/{something_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete something",
    description="Delete something with ownership validation and cascade cleanup"
)
async def delete_something(
    something_id: int,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Delete a something with ownership validation.

    Cascade deletes SomethingCircle junction table entries.

    **Returns:**
    - 204 No Content on success
    - 404 Not Found if something doesn't exist or doesn't belong to user
    """
    try:
        user_uuid = UUID(user_id)

        something = (
            db.query(Something)
            .filter(
                Something.id == something_id,
                Something.user_id == user_uuid
            )
            .first()
        )

        if not something:
            logger.warning(f"Something {something_id} not found for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Something with id {something_id} not found"
            )

        # Delete something (cascade deletes SomethingCircle entries)
        db.delete(something)
        db.commit()

        logger.info(f"Deleted something {something_id} for user {user_id}")

        # Return 204 No Content (no response body)
        return None

    except ValueError as e:
        logger.error(f"Invalid UUID format: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid user ID format: {str(e)}"
        )
