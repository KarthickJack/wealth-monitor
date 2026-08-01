import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PartyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)


class PartyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID | None
    name: str
    is_system: bool
    created_at: datetime
