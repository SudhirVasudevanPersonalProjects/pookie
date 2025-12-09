from pydantic import BaseModel, Field, ConfigDict, field_serializer
from datetime import datetime
from typing import Optional, List
from enum import Enum
from uuid import UUID


class ContentType(str, Enum):
    text = "text"
    image = "image"
    video = "video"
    url = "url"


class SomethingBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    content: Optional[str] = None
    content_type: ContentType = Field(alias="contentType", default=ContentType.text)
    media_url: Optional[str] = Field(alias="mediaUrl", default=None)


class SomethingCreate(SomethingBase):
    pass


class CirclePrediction(BaseModel):
    """Circle prediction from centroid similarity."""
    model_config = ConfigDict(populate_by_name=True)

    circle_id: int = Field(alias="circleId")
    circle_name: str = Field(alias="circleName")
    confidence: float


class SomethingResponse(SomethingBase):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int
    user_id: UUID | str = Field(alias="userId")
    meaning: Optional[str] = None
    is_meaning_user_edited: bool = Field(alias="isMeaningUserEdited", default=False)
    novelty_score: Optional[float] = Field(alias="noveltyScore", default=None, ge=0.0, le=1.0)
    suggested_circles: List[CirclePrediction] = Field(alias="suggestedCircles", default_factory=list)
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    @field_serializer('user_id')
    def serialize_user_id(self, user_id: UUID | str) -> str:
        """Convert UUID to string for JSON serialization."""
        return str(user_id)


class SomethingUpdateMeaning(BaseModel):
    meaning: str
