"""
Circles API endpoints with centroid-based organization.

Story MVP-1: Circle assignment, removal, and prediction endpoints
with reinforcement learning feedback through centroid updates.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.circle import Circle
from app.models.something import Something
from app.models.something_circle import SomethingCircle
from app.services.centroid_service import centroid_service
from app.services.embedding_service import embedding_service
from app.services.vector_service import vector_service
from loguru import logger

router = APIRouter()

# Constants
MAX_PREDICTION_RESULTS = 50  # Maximum predictions to return


@router.post(
    "/{circle_id}/somethings/{something_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Assign something to circle",
    description="Assign something to circle with centroid update and RL signal tracking"
)
async def assign_something_to_circle(
    circle_id: int,
    something_id: int,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Assign something to circle with centroid update.

    **Process:**
    1. Validate circle and something belong to user
    2. Check if assignment already exists (idempotent)
    3. Create SomethingCircle record with is_user_assigned=True
    4. Update circle centroid using something's embedding
    5. Return 204 No Content

    **Learning Signal:**
    - Sets is_user_assigned=True (high-quality RL signal)
    - Centroid shifts toward this something's embedding

    **Returns:**
    - 204 No Content on success
    - 404 if circle or something not found or doesn't belong to user
    - 400 if already assigned
    """
    try:
        user_uuid = UUID(user_id)

        # Validate circle belongs to user
        circle = (
            db.query(Circle)
            .filter(Circle.id == circle_id, Circle.user_id == user_uuid)
            .first()
        )
        if not circle:
            logger.warning(f"Circle {circle_id} not found for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Circle {circle_id} not found"
            )

        # Validate something belongs to user
        something = (
            db.query(Something)
            .filter(Something.id == something_id, Something.user_id == user_uuid)
            .first()
        )
        if not something:
            logger.warning(f"Something {something_id} not found for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Something {something_id} not found"
            )

        # Check if already assigned (idempotent)
        existing = (
            db.query(SomethingCircle)
            .filter(
                SomethingCircle.circle_id == circle_id,
                SomethingCircle.something_id == something_id
            )
            .first()
        )
        if existing:
            logger.info(f"Something {something_id} already assigned to circle {circle_id} (idempotent)")
            return None  # 204 No Content (idempotent success)

        # Create assignment with RL signal
        assignment = SomethingCircle(
            circle_id=circle_id,
            something_id=something_id,
            is_user_assigned=True,  # Learning signal: user manually assigned
            confidence_score=1.0  # User assignment = 100% confidence
        )
        db.add(assignment)

        # Validate something has non-empty content
        if not something.content or not something.content.strip():
            logger.warning(f"Something {something_id} has empty content, cannot assign to circle")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot assign something with empty content to circle. Content is required for centroid calculation."
            )

        # Update circle centroid with something's embedding (in same transaction)
        # Generate embedding if we don't have it
        embedding = embedding_service.generate_embedding(something.content)
        # Pass commit=False to keep transaction open
        centroid_service.update_centroid_add(circle_id, embedding, db, commit=False)
        logger.info(f"Updated centroid for circle {circle_id} after assignment")

        # Commit both assignment and centroid update atomically
        db.commit()
        logger.info(f"Assigned something {something_id} to circle {circle_id} (user_assigned=True)")

        return None  # 204 No Content

    except ValueError as e:
        logger.error(f"Invalid UUID format: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid user ID format: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to assign something to circle: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to assign something to circle"
        )


@router.delete(
    "/{circle_id}/somethings/{something_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove something from circle",
    description="Remove something from circle with centroid update"
)
async def remove_something_from_circle(
    circle_id: int,
    something_id: int,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Remove something from circle with centroid update.

    **Process:**
    1. Validate circle and something belong to user
    2. Find and delete SomethingCircle record
    3. Update circle centroid (remove this something's influence)
    4. Return 204 No Content

    **Centroid Update:**
    - Reverses the add operation using incremental formula
    - If last item removed, centroid becomes NULL

    **Returns:**
    - 204 No Content on success
    - 404 if circle, something, or assignment not found
    """
    try:
        user_uuid = UUID(user_id)

        # Validate circle belongs to user
        circle = (
            db.query(Circle)
            .filter(Circle.id == circle_id, Circle.user_id == user_uuid)
            .first()
        )
        if not circle:
            logger.warning(f"Circle {circle_id} not found for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Circle {circle_id} not found"
            )

        # Validate something belongs to user
        something = (
            db.query(Something)
            .filter(Something.id == something_id, Something.user_id == user_uuid)
            .first()
        )
        if not something:
            logger.warning(f"Something {something_id} not found for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Something {something_id} not found"
            )

        # Find assignment
        assignment = (
            db.query(SomethingCircle)
            .filter(
                SomethingCircle.circle_id == circle_id,
                SomethingCircle.something_id == something_id
            )
            .first()
        )
        if not assignment:
            logger.warning(f"Assignment not found: something {something_id} not in circle {circle_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Something {something_id} is not assigned to circle {circle_id}"
            )

        # Get embedding for centroid update
        # Note: In production, store embeddings in Something table to avoid regeneration
        # For MVP, we regenerate (100-200ms acceptable for remove operations)
        embedding = None
        if something.content and something.content.strip():
            embedding = embedding_service.generate_embedding(something.content)

        # Delete assignment
        db.delete(assignment)

        # Update circle centroid (remove this something's influence) - same transaction
        if embedding is not None:
            # Pass commit=False to keep transaction open
            centroid_service.update_centroid_remove(circle_id, embedding, db, commit=False)
            logger.info(f"Updated centroid for circle {circle_id} after removal")
        else:
            logger.warning(f"Something {something_id} has no content for embedding, skipping centroid update")

        # Commit both deletion and centroid update atomically
        db.commit()
        logger.info(f"Removed something {something_id} from circle {circle_id}")

        return None  # 204 No Content

    except ValueError as e:
        logger.error(f"Invalid UUID format: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid user ID format: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to remove something from circle: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove something from circle"
        )


@router.get(
    "/{circle_id}/predict-similar",
    summary="Get similar somethings for circle",
    description="Find somethings similar to circle's centroid for auto-suggestion"
)
async def get_predict_similar(
    circle_id: int,
    top_k: int = 10,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get somethings similar to circle's centroid.

    Uses circle's centroid to find semantically similar somethings
    that might belong in this circle.

    **Query Parameters:**
    - top_k: Number of suggestions to return (default: 10, max: 50)

    **Returns:**
    - List of somethings with similarity scores
    - Empty list if circle has no centroid yet

    **Use Cases:**
    - Auto-suggest somethings to add to circle
    - Help user organize existing somethings
    - Discover related content
    """
    try:
        user_uuid = UUID(user_id)

        # Validate circle belongs to user
        circle = (
            db.query(Circle)
            .filter(Circle.id == circle_id, Circle.user_id == user_uuid)
            .first()
        )
        if not circle:
            logger.warning(f"Circle {circle_id} not found for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Circle {circle_id} not found"
            )

        # Check if circle has centroid
        if circle.centroid_embedding is None:
            logger.info(f"Circle {circle_id} has no centroid yet, returning empty suggestions")
            return {"suggestions": []}

        # Limit top_k to reasonable range
        top_k = min(max(1, top_k), MAX_PREDICTION_RESULTS)

        # Use FAISS vector search with circle centroid as query
        logger.info(f"Finding {top_k} somethings similar to circle {circle_id} centroid using FAISS")

        # Get IDs of somethings already in this circle
        assigned_something_ids = set(
            row[0] for row in db.query(SomethingCircle.something_id)
            .filter(SomethingCircle.circle_id == circle_id)
            .all()
        )

        # Search FAISS index using centroid
        # Request more than top_k to account for filtering
        search_limit = min(top_k * 3, 150)  # Over-fetch to compensate for filtering
        faiss_results = await vector_service.search_similar(
            circle.centroid_embedding,
            top_k=search_limit
        )

        # Filter and format results
        suggestions = []
        for something_id, similarity in faiss_results:
            # Skip if already in circle
            if something_id in assigned_something_ids:
                continue

            # Fetch something and verify ownership
            something = (
                db.query(Something)
                .filter(Something.id == something_id, Something.user_id == user_uuid)
                .first()
            )

            # Skip if not found or not owned by user
            if not something:
                continue

            suggestions.append({
                "somethingId": something.id,
                "content": something.content,
                "similarity": round(float(similarity), 3)
            })

            # Stop once we have enough suggestions
            if len(suggestions) >= top_k:
                break

        logger.info(f"Returning {len(suggestions)} FAISS-based suggestions for circle {circle_id}")

        return {"suggestions": suggestions}

    except ValueError as e:
        logger.error(f"Invalid UUID format: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid user ID format: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Failed to get similar somethings: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get similar somethings"
        )
