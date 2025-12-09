"""
Intentions CRUD API endpoints.

Story MVP-3: Provides RESTful API for creating, reading, updating, and deleting intentions
with many-to-many linking to somethings (intention_cares junction).
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.intention import Intention
from app.models.intention_care import IntentionCare
from app.models.something import Something
from app.models.action_intention import ActionIntention
from app.models.action import Action
from app.schemas.intention import (
    IntentionCreate,
    IntentionUpdate,
    IntentionResponse,
    IntentionDetailResponse,
    SomethingBrief,
    ActionBrief,
)
from app.schemas.intention_care import IntentionCareLinkRequest
from loguru import logger

router = APIRouter()


@router.post(
    "",
    response_model=IntentionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new intention",
    description="Create a new intention (action-oriented goal) for the authenticated user"
)
async def create_intention(
    intention_data: IntentionCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Create new intention.

    **Process:**
    1. Create intention in database with active status
    2. Return created intention

    **Returns:**
    - 201 Created with IntentionResponse
    """
    try:
        # Convert user_id string to UUID
        user_uuid = UUID(user_id)

        # Create intention in database
        db_intention = Intention(
            user_id=user_uuid,
            intention_text=intention_data.intention_text,
            status="active"
        )
        db.add(db_intention)
        db.commit()
        db.refresh(db_intention)

        logger.info(f"Created intention {db_intention.id} for user {user_id}")

        return IntentionResponse.model_validate(db_intention)

    except Exception as e:
        logger.error(f"Failed to create intention: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create intention"
        )


@router.get(
    "",
    response_model=List[IntentionResponse],
    summary="List all intentions",
    description="Get all intentions for the authenticated user, ordered by creation date"
)
async def list_intentions(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    List all user intentions, grouped by status.

    **Returns:**
    - List of intentions ordered by: status (active, completed, archived), then created_at DESC
    """
    try:
        user_uuid = UUID(user_id)

        # Query intentions for user, ordered by status and creation date
        intentions = db.scalars(
            select(Intention)
            .where(Intention.user_id == user_uuid)
            .order_by(
                Intention.status.desc(),  # active > completed > archived (alphabetically descending)
                Intention.created_at.desc()
            )
        ).all()

        logger.info(f"Retrieved {len(intentions)} intentions for user {user_id}")

        return [IntentionResponse.model_validate(i) for i in intentions]

    except Exception as e:
        logger.error(f"Failed to list intentions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve intentions"
        )


@router.get(
    "/{intention_id}",
    response_model=IntentionDetailResponse,
    summary="Get intention detail",
    description="Get intention with linked somethings (cares) and actions"
)
async def get_intention_detail(
    intention_id: int,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get intention detail with all linked somethings and actions.

    **Returns:**
    - IntentionDetailResponse with linked_somethings and linked_actions
    - 404 if intention not found or doesn't belong to user
    """
    try:
        user_uuid = UUID(user_id)

        # Query intention with joins
        intention = db.scalar(
            select(Intention)
            .options(
                joinedload(Intention.intention_cares).joinedload(IntentionCare.something),
                joinedload(Intention.actions).joinedload(ActionIntention.action)
            )
            .where(Intention.id == intention_id, Intention.user_id == user_uuid)
        )

        if not intention:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Intention {intention_id} not found"
            )

        # Build linked somethings list
        linked_somethings = [
            SomethingBrief(
                id=ic.something.id,
                content=ic.something.content,
                meaning=ic.something.meaning
            )
            for ic in intention.intention_cares
        ]

        # Build linked actions list
        linked_actions = [
            ActionBrief(
                id=ai.action.id,
                action_text=ai.action.action_text,
                time_elapsed=ai.action.time_elapsed,
                completed_at=ai.action.completed_at
            )
            for ai in intention.actions
        ]

        # Build response
        response = IntentionDetailResponse(
            id=intention.id,
            user_id=str(intention.user_id),
            intention_text=intention.intention_text,
            status=intention.status,
            created_at=intention.created_at,
            updated_at=intention.updated_at,
            linked_somethings=linked_somethings,
            linked_actions=linked_actions
        )

        logger.info(f"Retrieved intention {intention_id} with {len(linked_somethings)} somethings and {len(linked_actions)} actions")

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get intention detail: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve intention detail"
        )


@router.put(
    "/{intention_id}",
    response_model=IntentionResponse,
    summary="Update intention",
    description="Update intention text and/or status"
)
async def update_intention(
    intention_id: int,
    update_data: IntentionUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Update intention text and/or status.

    **Returns:**
    - Updated IntentionResponse
    - 404 if intention not found or doesn't belong to user
    """
    try:
        user_uuid = UUID(user_id)

        # Find intention
        intention = db.scalar(
            select(Intention)
            .where(Intention.id == intention_id, Intention.user_id == user_uuid)
        )

        if not intention:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Intention {intention_id} not found"
            )

        # Update fields if provided
        if update_data.intention_text is not None:
            intention.intention_text = update_data.intention_text
            logger.info(f"Updated intention {intention_id} text")

        if update_data.status is not None:
            intention.status = update_data.status.value
            logger.info(f"Updated intention {intention_id} status to {update_data.status.value}")

        db.commit()
        db.refresh(intention)

        return IntentionResponse.model_validate(intention)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update intention: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update intention"
        )


@router.delete(
    "/{intention_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete intention",
    description="Delete intention and cascade to junction tables (preserves somethings and actions)"
)
async def delete_intention(
    intention_id: int,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Delete intention.

    **Cascade behavior:**
    - Deletes IntentionCares (links to somethings) ← CASCADE
    - Deletes ActionIntentions (links to actions) ← CASCADE
    - Preserves Somethings (data remains)
    - Preserves Actions (data remains)

    **Returns:**
    - 204 No Content on success
    - 404 if intention not found or doesn't belong to user
    """
    try:
        user_uuid = UUID(user_id)

        # Find intention
        intention = db.scalar(
            select(Intention)
            .where(Intention.id == intention_id, Intention.user_id == user_uuid)
        )

        if not intention:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Intention {intention_id} not found"
            )

        # Delete (cascade deletes junction table entries)
        db.delete(intention)
        db.commit()

        logger.info(f"Deleted intention {intention_id} for user {user_id}")

        return None

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete intention: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete intention"
        )


@router.post(
    "/{intention_id}/link-cares",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Link somethings to intention",
    description="Bulk link multiple somethings (cares) to an intention"
)
async def link_cares_to_intention(
    intention_id: int,
    link_request: IntentionCareLinkRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Link multiple somethings to an intention.

    **Process:**
    1. Verify intention exists and belongs to user
    2. Verify all somethings exist and belong to user
    3. Create IntentionCare links (skip duplicates)

    **Returns:**
    - 204 No Content on success
    - 404 if intention or any something not found
    """
    try:
        user_uuid = UUID(user_id)

        # Verify intention exists and belongs to user
        intention = db.scalar(
            select(Intention)
            .where(Intention.id == intention_id, Intention.user_id == user_uuid)
        )

        if not intention:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Intention {intention_id} not found"
            )

        # Verify all somethings exist and belong to user
        somethings = db.scalars(
            select(Something)
            .where(Something.id.in_(link_request.something_ids), Something.user_id == user_uuid)
        ).all()

        if len(somethings) != len(link_request.something_ids):
            found_ids = {s.id for s in somethings}
            missing_ids = set(link_request.something_ids) - found_ids
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Somethings not found: {missing_ids}"
            )

        # Get existing links to avoid duplicates
        existing_links = db.scalars(
            select(IntentionCare.something_id)
            .where(
                IntentionCare.intention_id == intention_id,
                IntentionCare.something_id.in_(link_request.something_ids)
            )
        ).all()
        existing_something_ids = set(existing_links)

        # Create new links (skip duplicates)
        new_links = []
        for something_id in link_request.something_ids:
            if something_id not in existing_something_ids:
                new_link = IntentionCare(
                    intention_id=intention_id,
                    something_id=something_id
                )
                new_links.append(new_link)

        if new_links:
            db.add_all(new_links)
            db.commit()
            logger.info(f"Linked {len(new_links)} somethings to intention {intention_id}")
        else:
            logger.info(f"All somethings already linked to intention {intention_id}")

        return None

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to link cares to intention: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to link somethings to intention"
        )


@router.delete(
    "/{intention_id}/unlink-care/{something_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Unlink something from intention",
    description="Remove a single something link from an intention"
)
async def unlink_care_from_intention(
    intention_id: int,
    something_id: int,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Unlink a something from an intention.

    **Returns:**
    - 204 No Content on success (even if link didn't exist)
    - 404 if intention doesn't exist or doesn't belong to user
    """
    try:
        user_uuid = UUID(user_id)

        # Verify intention exists and belongs to user
        intention = db.scalar(
            select(Intention)
            .where(Intention.id == intention_id, Intention.user_id == user_uuid)
        )

        if not intention:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Intention {intention_id} not found"
            )

        # Find and delete link
        link = db.scalar(
            select(IntentionCare)
            .where(
                IntentionCare.intention_id == intention_id,
                IntentionCare.something_id == something_id
            )
        )

        if link:
            db.delete(link)
            db.commit()
            logger.info(f"Unlinked something {something_id} from intention {intention_id}")
        else:
            logger.info(f"Link already removed: something {something_id} from intention {intention_id}")

        return None

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to unlink care from intention: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to unlink something from intention"
        )
