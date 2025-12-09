from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base


class ActionIntention(Base):
    """
    Junction table linking actions to intentions (many-to-many).

    One action can fulfill multiple intentions.
    Example: "30min run" fulfills both "Get fit" AND "Train for marathon"

    When an intention is deleted, Pookie should ask the user why
    (handled in application logic, not database).
    """
    __tablename__ = "action_intentions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    action_id = Column(Integer, ForeignKey("actions.id", ondelete="CASCADE"), nullable=False, index=True)
    intention_id = Column(Integer, ForeignKey("intentions.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    action = relationship("Action", back_populates="intentions")
    intention = relationship("Intention", back_populates="actions")

    # Constraint: Prevent duplicate action-intention links
    __table_args__ = (
        UniqueConstraint('action_id', 'intention_id', name='uq_action_intention'),
    )

    def __repr__(self):
        return f"<ActionIntention(action_id={self.action_id}, intention_id={self.intention_id})>"
