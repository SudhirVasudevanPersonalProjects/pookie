"""
Pydantic schemas for chat endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional


class ChatQueryRequest(BaseModel):
    """Request schema for streaming chat."""

    query: str = Field(..., min_length=1, max_length=500, description="User's question")
    top_k: Optional[int] = Field(default=10, ge=1, le=50, description="Number of somethings to retrieve")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "query": "What fitness goals have I set?",
                    "top_k": 10
                }
            ]
        }
    }
