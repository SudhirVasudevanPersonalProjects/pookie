from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base


class IntentionCare(Base):
    """
    Junction table linking intentions to somethings (many-to-many).

    Represents which somethings (captures) relate to which intentions (goals).
    Example: Intention "Get fit" ← linked to → Somethings: "I want abs", "Gym motivation"
    """
    __tablename__ = "intention_cares"

    id = Column(Integer, primary_key=True, autoincrement=True)
    intention_id = Column(Integer, ForeignKey("intentions.id", ondelete="CASCADE"), nullable=False, index=True)
    something_id = Column(Integer, ForeignKey("somethings.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    intention = relationship("Intention", back_populates="intention_cares")
    something = relationship("Something", back_populates="intention_cares")

    # Constraint: Prevent duplicate links
    __table_args__ = (
        UniqueConstraint('intention_id', 'something_id', name='uq_intention_something'),
    )

    def __repr__(self):
        return f"<IntentionCare(intention_id={self.intention_id}, something_id={self.something_id})>"
