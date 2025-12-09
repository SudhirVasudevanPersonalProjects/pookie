from sqlalchemy import Column, Integer, Text, Float, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base


class Something(Base):
    """
    Somethings are user-captured items that can be text, images, videos, or URLs.

    Voice notes are converted to text via voice-to-text.
    Images/videos are stored in Supabase Storage with URLs saved here.

    The 'meaning' field contains LLM-generated reasoning/interpretation about
    why this something matters or what it represents. Users can edit this,
    and the LLM learns from user edits via the is_meaning_user_edited flag.
    """
    __tablename__ = "somethings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    content = Column(Text, nullable=True)  # Text content (nullable if only media)
    content_type = Column(
        Enum('text', 'image', 'video', 'url', name='content_type'),
        default='text',
        nullable=False
    )
    media_url = Column(Text, nullable=True)  # URL to Supabase Storage or external URL
    meaning = Column(Text, nullable=True)  # LLM-generated reasoning/interpretation
    is_meaning_user_edited = Column(Boolean, default=False, nullable=False)  # Learning signal
    novelty_score = Column(Float, nullable=True)  # Importance ranking 0-1
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="somethings")
    circles = relationship("SomethingCircle", back_populates="something", cascade="all, delete-orphan")
    intention_cares = relationship("IntentionCare", back_populates="something", cascade="all, delete-orphan")

    def __repr__(self):
        content_preview = (self.content[:30] + '...') if self.content else '[media]'
        return f"<Something(id={self.id}, type={self.content_type}, content='{content_preview}')>"
