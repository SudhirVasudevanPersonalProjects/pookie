"""
Pytest fixtures for testing.

Provides test database, client, and authentication fixtures.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import uuid

from app.main import app
from app.core.database import get_db
from app.core.config import settings
from app.models.base import Base
from app.models.user import User
from app.models.something import Something


@pytest.fixture(scope="function")
def db_engine():
    """Create a test database engine using the configured DATABASE_URL."""
    # Use the real PostgreSQL database from settings
    engine = create_engine(settings.DATABASE_URL)

    # Create all tables (if they don't exist)
    Base.metadata.create_all(bind=engine)

    yield engine

    # Note: We don't drop tables after tests to preserve data across runs
    # Individual tests should clean up their own data if needed


@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator[Session, None, None]:
    """Create a test database session that commits to the real database."""
    # Create session without transaction wrapping
    # This allows test data to be visible to API endpoints
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = TestSessionLocal()

    try:
        yield session
    finally:
        # Note: Tests are responsible for cleaning up their own data
        # or we rely on unique IDs/emails to avoid conflicts
        session.close()


@pytest.fixture(scope="function")
def client() -> Generator[TestClient, None, None]:
    """Create a test client that uses the real database connection."""
    # Don't override get_db - let the app use its normal database connection
    # This ensures API endpoints see the same data as test fixtures
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db_session: Session) -> User:
    """Create a test user in the database with unique ID and email per test."""
    user_id = uuid.uuid4()
    user = User(
        id=user_id,
        email=f"test-{user_id}@example.com"  # Unique email per test
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_user_id(test_user: User) -> str:
    """Get the test user's UUID as a string."""
    return str(test_user.id)


@pytest.fixture(scope="function")
def other_user(db_session: Session) -> User:
    """Create another test user for isolation testing."""
    user_id = uuid.uuid4()
    user = User(
        id=user_id,
        email=f"other-{user_id}@example.com"  # Unique email per test
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def other_user_id(other_user: User) -> str:
    """Get the other user's UUID as a string."""
    return str(other_user.id)


@pytest.fixture(scope="function")
def mock_auth_headers(test_user_id: str):
    """
    Mock JWT authentication to bypass Supabase validation in tests.

    Returns headers dict with fake JWT token.
    """
    from app.core.security import get_current_user_id

    async def override_get_current_user_id():
        """Mock authentication dependency that returns test user ID."""
        return test_user_id

    # Override the FastAPI dependency
    app.dependency_overrides[get_current_user_id] = override_get_current_user_id

    headers = {"Authorization": f"Bearer fake-jwt-token-{test_user_id}"}

    yield headers

    # Clean up override
    if get_current_user_id in app.dependency_overrides:
        del app.dependency_overrides[get_current_user_id]


@pytest.fixture(scope="function")
def mock_other_auth_headers(other_user_id: str):
    """Mock JWT authentication for the other user."""
    from app.core.security import get_current_user_id

    async def override_get_current_user_id():
        """Mock authentication dependency that returns other user ID."""
        return other_user_id

    app.dependency_overrides[get_current_user_id] = override_get_current_user_id

    headers = {"Authorization": f"Bearer fake-jwt-token-{other_user_id}"}

    yield headers

    # Clean up override
    if get_current_user_id in app.dependency_overrides:
        del app.dependency_overrides[get_current_user_id]


# --- Additional Test Data Fixtures ---

@pytest.fixture(scope="function")
def create_test_something(db_session: Session):
    """Factory fixture to create test somethings."""
    def _create_something(user_id: uuid.UUID, content: str = "Test thought", meaning: str = None):
        from app.models.something import Something
        something = Something(
            user_id=user_id,
            content=content,
            meaning=meaning
        )
        db_session.add(something)
        db_session.commit()
        db_session.refresh(something)
        return something
    return _create_something


@pytest.fixture(scope="function")
def create_test_intention(db_session: Session):
    """Factory fixture to create test intentions."""
    def _create_intention(user_id: uuid.UUID, intention_text: str = "Test intention", status: str = "active"):
        from app.models.intention import Intention
        intention = Intention(
            user_id=user_id,
            intention_text=intention_text,
            status=status
        )
        db_session.add(intention)
        db_session.commit()
        db_session.refresh(intention)
        return intention
    return _create_intention


@pytest.fixture(scope="function")
def test_intention_data():
    """Sample intention data for testing."""
    return {
        "intentionText": "Complete the project on time",
        "status": "active"
    }


