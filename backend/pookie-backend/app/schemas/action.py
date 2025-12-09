from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from typing import Optional, List
from uuid import UUID


class ActionCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    action_text: str = Field(alias="actionText", min_length=1, max_length=500)
    time_elapsed: int = Field(alias="timeElapsed", ge=0, le=360)
    intention_ids: Optional[List[int]] = Field(alias="intentionIds", default=None)


class ActionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int
    user_id: UUID | str = Field(alias="userId")
    action_text: str = Field(alias="actionText")
    time_elapsed: int = Field(alias="timeElapsed")
    completed_at: datetime = Field(alias="completedAt")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    @field_validator('user_id')
    @classmethod
    def serialize_user_id(cls, v: UUID | str) -> str:
        """Convert UUID to string for JSON serialization."""
        return str(v)
