from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base


class StoryAction(Base):
    """
    Junction table linking stories to actions (many-to-many).

    Stories are narrative summaries that combine multiple actions.
    Example: Story "This week I crushed my fitness goals!" links to:
      - Action "Gym session - 60min"
      - Action "Morning run - 45min"
      - Action "Yoga class - 30min"

    If an action is deleted:
      - CASCADE deletes this link
      - Application logic should check if story has 0 actions remaining
      - If yes, delete the story (Option A: Application cleanup)
    """
    __tablename__ = "story_actions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    story_id = Column(Integer, ForeignKey("stories.id", ondelete="CASCADE"), nullable=False, index=True)
    action_id = Column(Integer, ForeignKey("actions.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    story = relationship("Story", back_populates="actions")
    action = relationship("Action", back_populates="stories")

    # Constraint: Prevent duplicate story-action links
    __table_args__ = (
        UniqueConstraint('story_id', 'action_id', name='uq_story_action'),
    )

    def __repr__(self):
        return f"<StoryAction(story_id={self.story_id}, action_id={self.action_id})>"
