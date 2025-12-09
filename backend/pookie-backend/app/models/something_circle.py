from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base


class SomethingCircle(Base):
    """
    Junction table linking somethings to circles (many-to-many).

    One something can belong to multiple circles.
    Tracks whether the user manually assigned the circle (high confidence)
    or if it was LLM-suggested (has confidence_score).

    The LLM learns from is_user_assigned=True entries to improve future predictions.
    """
    __tablename__ = "something_circles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    something_id = Column(Integer, ForeignKey("somethings.id", ondelete="CASCADE"), nullable=False, index=True)
    circle_id = Column(Integer, ForeignKey("circles.id", ondelete="CASCADE"), nullable=False, index=True)
    is_user_assigned = Column(Boolean, default=False, nullable=False)  # Learning signal
    confidence_score = Column(Float, nullable=True)  # LLM confidence (0-1) if auto-assigned
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    something = relationship("Something", back_populates="circles")
    circle = relationship("Circle", back_populates="somethings")

    # Constraint: Prevent duplicate something-circle links
    __table_args__ = (
        UniqueConstraint('something_id', 'circle_id', name='uq_something_circle'),
    )

    def __repr__(self):
        assigned_by = "user" if self.is_user_assigned else f"llm({self.confidence_score:.2f})"
        return f"<SomethingCircle(something_id={self.something_id}, circle_id={self.circle_id}, {assigned_by})>"
