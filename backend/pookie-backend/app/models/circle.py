from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, ARRAY, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func, text
from sqlalchemy.orm import relationship
from app.models.base import Base


class Circle(Base):
    __tablename__ = "circles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    circle_name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    care_frequency = Column(Integer, server_default=text('0'), nullable=False)  # Database-side DEFAULT 0
    centroid_embedding = Column(ARRAY(Float), nullable=True)  # 384-dim vector for circle centroid
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="circles")
    somethings = relationship("SomethingCircle", back_populates="circle", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Circle(id={self.id}, name='{self.circle_name}')>"
