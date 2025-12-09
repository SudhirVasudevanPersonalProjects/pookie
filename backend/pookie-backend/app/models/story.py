from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base


class Story(Base):
    """
    Stories are narrative summaries combining multiple actions.

    Example: "This week I crushed my fitness goals!"
    Links to multiple actions via story_actions junction table.

    Stories no longer have a direct intention_id FK.
    They connect to intentions through actions.

    If all actions are deleted from a story:
      - Application logic should delete the story (Option A cleanup strategy)
    """
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    story_text = Column(Text, nullable=False)  # Narrative summary
    completed_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="stories")
    actions = relationship("StoryAction", back_populates="story", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Story(id={self.id}, user_id={self.user_id}, text='{self.story_text[:30]}...')>"
