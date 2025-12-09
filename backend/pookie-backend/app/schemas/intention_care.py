from pydantic import BaseModel, Field, ConfigDict
from typing import List


class IntentionCareLinkRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    something_ids: List[int] = Field(alias="somethingIds", min_length=1)
