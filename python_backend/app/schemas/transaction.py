import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class TransactionCreate(BaseModel):
    transaction_date: datetime
    transaction_type: int = Field(ge=0, le=1)
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    party_id: uuid.UUID | None = None
    category_id: uuid.UUID | None = None
    description: str | None = Field(default=None, max_length=500)


class TransactionUpdate(BaseModel):
    transaction_date: datetime | None = None
    transaction_type: int | None = Field(default=None, ge=0, le=1)
    amount: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=2)
    party_id: uuid.UUID | None = None
    category_id: uuid.UUID | None = None
    description: str | None = Field(default=None, max_length=500)


class TransactionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    transaction_date: datetime
    transaction_type: int
    amount: Decimal
    party_id: uuid.UUID | None
    category_id: uuid.UUID | None
    description: str | None
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
