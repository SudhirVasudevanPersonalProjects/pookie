from pydantic import BaseModel, Field, ConfigDict, field_serializer
from datetime import datetime, timezone
from typing import Optional, List
from enum import Enum
from uuid import UUID


class ContentType(str, Enum):
    text = "text"
    image = "image"
    video = "video"
    url = "url"


class SomethingBase(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    content: Optional[str] = None
    content_type: ContentType = Field(default=ContentType.text, serialization_alias="contentType")
    media_url: Optional[str] = Field(default=None, serialization_alias="mediaUrl")


class SomethingCreate(SomethingBase):
    pass


class CirclePrediction(BaseModel):
    """Circle prediction from centroid similarity."""

    circle_id: int = Field(serialization_alias="circleId")
    circle_name: str = Field(serialization_alias="circleName")
    confidence: float


class SomethingResponse(SomethingBase):
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True
    )

    id: int
    user_id: UUID | str = Field(serialization_alias="userId")
    meaning: Optional[str] = None
    is_meaning_user_edited: bool = Field(default=False, serialization_alias="isMeaningUserEdited")
    novelty_score: Optional[float] = Field(default=None, ge=0.0, le=1.0, serialization_alias="noveltyScore")
    suggested_circles: List[CirclePrediction] = Field(default_factory=list, serialization_alias="suggestedCircles")
    created_at: datetime = Field(serialization_alias="createdAt")
    updated_at: datetime = Field(serialization_alias="updatedAt")

    @field_serializer('user_id')
    def serialize_user_id(self, user_id: UUID | str) -> str:
        """Convert UUID to string for JSON serialization."""
        return str(user_id)

    @field_serializer('created_at')
    def serialize_datetime(self, created_at: datetime) -> str:
        """Ensure datetime is always ISO8601 string for JSON output."""
        return created_at.isoformat(timespec="microseconds").replace("+00:00", "Z")

    
    @field_serializer('updated_at')
    def serialize_datetime(self, updated_at: datetime) -> str:
        """Ensure datetime is always ISO8601 string for JSON output."""
        return updated_at.isoformat(timespec="microseconds").replace("+00:00", "Z")

class SomethingUpdateMeaning(BaseModel):
    meaning: str
