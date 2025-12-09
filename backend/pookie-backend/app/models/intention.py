from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base


class Intention(Base):
    __tablename__ = "intentions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    intention_text = Column(Text, nullable=False)
    status = Column(Enum('active', 'completed', 'archived', name='intention_status'), default='active', nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="intentions")
    intention_cares = relationship("IntentionCare", back_populates="intention", cascade="all, delete-orphan")
    actions = relationship("ActionIntention", back_populates="intention", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Intention(id={self.id}, text='{self.intention_text[:30]}...', status={self.status})>"
