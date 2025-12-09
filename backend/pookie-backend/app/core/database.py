"""
Database session management for SQLAlchemy.

Provides dependency injection for database sessions in FastAPI endpoints.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from app.core.config import settings


# Create database engine
# pool_pre_ping=True enables connection health checks before each use
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG  # Log SQL statements in debug mode
)

# Create session factory
# autocommit=False, autoflush=False: Manual control over transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session.

    Usage in endpoints:
        @router.get("/somethings")
        async def list_somethings(db: Session = Depends(get_db)):
            ...

    The session is automatically closed after the request completes,
    ensuring proper cleanup even if exceptions occur.

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
