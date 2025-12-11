"""
JWT Authentication middleware using Supabase.

Validates JWT tokens from iOS clients and provides authenticated user context.
"""
import logging
from typing import Optional
from functools import lru_cache

from supabase import create_client, Client
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings

logger = logging.getLogger(__name__)

# HTTPBearer security scheme for automatic token extraction
security = HTTPBearer()


@lru_cache()
def get_supabase_client() -> Client:
    """
    Create and cache Supabase client with service_role key.

    Uses lazy initialization to avoid crashes if env vars are missing at import time.
    """
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    """
    Validate JWT token and return user info.

    Args:
        credentials: HTTP Bearer token from Authorization header

    Returns:
        dict: User object with id, email, and other claims

    Raises:
        HTTPException: 401 if token is invalid, expired, or malformed
    """
    token = credentials.credentials
    supabase = get_supabase_client()

    try:
        # Verify JWT token with Supabase
        user = supabase.auth.get_user(token)

        # Log successful authentication
        user_id = _extract_user_id(user)
        logger.info(f"User authenticated successfully: {user_id}")

        return user
    except AttributeError as e:
        # Supabase SDK configuration error
        logger.error(f"Supabase client configuration error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Authentication service configuration error"
        )
    except ValueError as e:
        # Invalid token format
        logger.warning(f"Invalid token format: {str(e)}")
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )
    except Exception as e:
        # Network errors, expired tokens, etc.
        logger.warning(f"Authentication failed for token: {token[:10]}... Error: {type(e).__name__}")
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )


def _extract_user_id(user) -> Optional[str]:
    """
    Safely extract user ID from Supabase user object.

    Handles multiple response formats from different Supabase SDK versions:
    - Direct object with .id attribute
    - Dict with "id" key
    - Nested user object (user.user.id or user["user"]["id"])

    Args:
        user: User object or dict from Supabase auth.get_user()

    Returns:
        str: User ID if found, None otherwise
    """
    # Try dict format first
    if isinstance(user, dict):
        if "id" in user:
            return user["id"]
        if "user" in user and isinstance(user["user"], dict):
            return user["user"].get("id")

    # Try object format
    if hasattr(user, "id"):
        return user.id

    # Try nested object format
    if hasattr(user, "user"):
        nested_user = user.user
        if isinstance(nested_user, dict):
            return nested_user.get("id")
        elif hasattr(nested_user, "id"):
            return nested_user.id

    return None


def _extract_user_email(user) -> Optional[str]:
    """
    Safely extract email from Supabase user object.

    Handles multiple response formats from different Supabase SDK versions:
    - Direct object with .email attribute
    - Dict with "email" key
    - Nested user object (user.user.email or user["user"]["email"])

    Args:
        user: User object or dict from Supabase auth.get_user()

    Returns:
        str: Email if found, None otherwise
    """
    # Try dict format first
    if isinstance(user, dict):
        if "email" in user:
            return user["email"]
        if "user" in user and isinstance(user["user"], dict):
            return user["user"].get("email")

    # Try object format
    if hasattr(user, "email"):
        return user.email

    # Try nested object format
    if hasattr(user, "user"):
        nested_user = user.user
        if isinstance(nested_user, dict):
            return nested_user.get("email")
        elif hasattr(nested_user, "email"):
            return nested_user.email

    return None


async def get_current_user_id(
    user: dict = Security(get_current_user)
) -> str:
    """
    Extract user ID from authenticated user and ensure user exists in database.

    Implements "just-in-time" user provisioning: creates user record on first auth.

    Args:
        user: Authenticated user from get_current_user dependency

    Returns:
        str: UUID of authenticated user

    Raises:
        HTTPException: 500 if user ID cannot be extracted or user creation fails
    """
    from sqlalchemy.orm import Session
    from app.core.database import get_db
    from app.models.user import User
    from uuid import UUID

    user_id = _extract_user_id(user)

    if not user_id:
        logger.error(f"Failed to extract user ID from user object: {type(user)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to extract user information"
        )

    # Extract email from user object
    email = _extract_user_email(user)
    if not email:
        logger.error(f"Failed to extract email from user object: {type(user)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to extract user email"
        )

    # Ensure user exists in database (just-in-time provisioning)
    # This is needed because Supabase manages authentication separately
    # from our application database
    db_gen = get_db()
    db = next(db_gen)
    try:
        user_uuid = UUID(user_id)

        # Check if user exists
        existing_user = db.query(User).filter(User.id == user_uuid).first()

        if not existing_user:
            # Create user record with ID from JWT token
            new_user = User(id=user_uuid, email=email)
            db.add(new_user)
            db.commit()
            logger.info(f"Created new user record for {user_id} ({email})")
        else:
            logger.debug(f"User {user_id} already exists in database")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to ensure user exists in database: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to provision user account"
        )
    finally:
        db.close()

    return user_id
