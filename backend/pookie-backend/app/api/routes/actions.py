"""
Actions CRUD API endpoints.

Story MVP-3: Provides RESTful API for creating, reading, and deleting actions
with many-to-many linking to intentions (action_intentions junction).
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.action import Action
from app.models.action_intention import ActionIntention
from app.models.intention import Intention
from app.schemas.action import ActionCreate, ActionResponse
from loguru import logger

router = APIRouter()


@router.post(
    "",
    response_model=ActionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new action",
    description="Create a new action (time-tracked activity) with optional intention links"
)
async def create_action(
    action_data: ActionCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Create new action with optional intention links.

    **Process:**
    1. Create action in database
    2. Link to intentions if intention_ids provided
    3. Return created action

    **Returns:**
    - 201 Created with ActionResponse
    """
    try:
        # Convert user_id string to UUID
        user_uuid = UUID(user_id)

        # Create action in database
        db_action = Action(
            user_id=user_uuid,
            action_text=action_data.action_text,
            time_elapsed=action_data.time_elapsed
        )
        db.add(db_action)
        db.commit()
        db.refresh(db_action)

        logger.info(f"Created action {db_action.id} for user {user_id}")

        # Link to intentions if provided
        if action_data.intention_ids:
            # Verify all intentions exist and belong to user
            intentions = db.scalars(
                select(Intention)
                .where(
                    Intention.id.in_(action_data.intention_ids),
                    Intention.user_id == user_uuid
                )
            ).all()

            if len(intentions) != len(action_data.intention_ids):
                found_ids = {i.id for i in intentions}
                missing_ids = set(action_data.intention_ids) - found_ids
                # Rollback action creation
                db.delete(db_action)
                db.commit()
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Intentions not found: {missing_ids}"
                )

            # Create action-intention links
            links = [
                ActionIntention(
                    action_id=db_action.id,
                    intention_id=intention_id
                )
                for intention_id in action_data.intention_ids
            ]
            db.add_all(links)
            db.commit()

            logger.info(f"Linked action {db_action.id} to {len(links)} intentions")

        return ActionResponse.model_validate(db_action)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create action: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create action"
        )


@router.get(
    "",
    response_model=List[ActionResponse],
    summary="List all actions",
    description="Get all actions for the authenticated user, ordered by completion date DESC"
)
async def list_actions(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    List all user actions, ordered by completed_at DESC.

    **Returns:**
    - List of actions ordered by most recent first
    """
    try:
        user_uuid = UUID(user_id)

        # Query actions for user, ordered by completion date
        actions = db.scalars(
            select(Action)
            .where(Action.user_id == user_uuid)
            .order_by(Action.completed_at.desc())
        ).all()

        logger.info(f"Retrieved {len(actions)} actions for user {user_id}")

        return [ActionResponse.model_validate(a) for a in actions]

    except Exception as e:
        logger.error(f"Failed to list actions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve actions"
        )


@router.get(
    "/{action_id}",
    response_model=ActionResponse,
    summary="Get action detail",
    description="Get action details"
)
async def get_action_detail(
    action_id: int,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get action detail.

    **Returns:**
    - ActionResponse
    - 404 if action not found or doesn't belong to user
    """
    try:
        user_uuid = UUID(user_id)

        # Query action
        action = db.scalar(
            select(Action)
            .where(Action.id == action_id, Action.user_id == user_uuid)
        )

        if not action:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Action {action_id} not found"
            )

        return ActionResponse.model_validate(action)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get action detail: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve action detail"
        )


@router.delete(
    "/{action_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete action",
    description="Delete action and cascade to junction tables (preserves intentions)"
)
async def delete_action(
    action_id: int,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Delete action.

    **Cascade behavior:**
    - Deletes ActionIntentions (links to intentions) ← CASCADE
    - Preserves Intentions (data remains)

    **Returns:**
    - 204 No Content on success
    - 404 if action not found or doesn't belong to user
    """
    try:
        user_uuid = UUID(user_id)

        # Find action
        action = db.scalar(
            select(Action)
            .where(Action.id == action_id, Action.user_id == user_uuid)
        )

        if not action:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Action {action_id} not found"
            )

        # Delete (cascade deletes junction table entries)
        db.delete(action)
        db.commit()

        logger.info(f"Deleted action {action_id} for user {user_id}")

        return None

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete action: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete action"
        )


@router.post(
    "/{action_id}/link-intention/{intention_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Link action to intention",
    description="Link an existing action to an existing intention"
)
async def link_action_to_intention(
    action_id: int,
    intention_id: int,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Link an existing action to an existing intention.

    **Process:**
    1. Verify action exists and belongs to user
    2. Verify intention exists and belongs to user
    3. Create ActionIntention link (skip if duplicate)

    **Returns:**
    - 204 No Content on success
    - 404 if action or intention not found
    """
    try:
        user_uuid = UUID(user_id)

        # Verify action exists and belongs to user
        action = db.scalar(
            select(Action)
            .where(Action.id == action_id, Action.user_id == user_uuid)
        )

        if not action:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Action {action_id} not found"
            )

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

        # Check if link already exists
        existing_link = db.scalar(
            select(ActionIntention)
            .where(
                ActionIntention.action_id == action_id,
                ActionIntention.intention_id == intention_id
            )
        )

        if not existing_link:
            # Create new link
            new_link = ActionIntention(
                action_id=action_id,
                intention_id=intention_id
            )
            db.add(new_link)
            db.commit()
            logger.info(f"Linked action {action_id} to intention {intention_id}")
        else:
            logger.info(f"Link already exists: action {action_id} to intention {intention_id}")

        return None

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to link action to intention: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to link action to intention"
        )
