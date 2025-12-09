from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base


class Action(Base):
    """
    Actions are time-tracked activities that fulfill intentions.

    Examples: "Went to gym - 60min", "Meditated - 20min"

    Actions can fulfill multiple intentions via the action_intentions junction table.
    Actions are combined into stories via the story_actions junction table.

    time_elapsed is stored in minutes (Integer).
    """
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    action_text = Column(Text, nullable=False)  # Description of what was done
    time_elapsed = Column(Integer, nullable=False)  # Duration in minutes
    completed_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="actions")
    intentions = relationship("ActionIntention", back_populates="action", cascade="all, delete-orphan")
    stories = relationship("StoryAction", back_populates="action", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Action(id={self.id}, text='{self.action_text[:30]}...', time={self.time_elapsed}min)>"
