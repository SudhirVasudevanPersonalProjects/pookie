from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from typing import Optional, List
from enum import Enum
from uuid import UUID


class IntentionStatus(str, Enum):
    active = "active"
    completed = "completed"
    archived = "archived"


class IntentionCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    intention_text: str = Field(alias="intentionText", min_length=1, max_length=500)


class IntentionUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    intention_text: Optional[str] = Field(alias="intentionText", default=None, min_length=1, max_length=500)
    status: Optional[IntentionStatus] = None


class SomethingBrief(BaseModel):
    """Brief something info for intention detail view."""
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int
    content: Optional[str] = None
    meaning: Optional[str] = None


class ActionBrief(BaseModel):
    """Brief action info for intention detail view."""
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int
    action_text: str = Field(alias="actionText")
    time_elapsed: int = Field(alias="timeElapsed")
    completed_at: datetime = Field(alias="completedAt")


class IntentionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int
    user_id: UUID | str = Field(alias="userId")
    intention_text: str = Field(alias="intentionText")
    status: IntentionStatus
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    @field_validator('user_id')
    @classmethod
    def serialize_user_id(cls, v: UUID | str) -> str:
        """Convert UUID to string for JSON serialization."""
        return str(v)


class IntentionDetailResponse(IntentionResponse):
    """Intention with linked somethings and actions."""
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    linked_somethings: List[SomethingBrief] = Field(alias="linkedSomethings", default_factory=list)
    linked_actions: List[ActionBrief] = Field(alias="linkedActions", default_factory=list)
