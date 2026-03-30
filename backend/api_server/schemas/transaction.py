from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class ItemInput(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    qty: Decimal = Field(gt=0)
    price: Decimal = Field(gt=0)

    @field_validator("name")
    @classmethod
    def sanitize_name(cls, value: str) -> str:
        return " ".join(value.strip().split()).lower()


class ConfirmTransactionRequest(BaseModel):
    customer_id: int | None = None
    items: list[ItemInput] = Field(default_factory=list)
    voice_data: dict | None = None
    transaction_type: Literal["credit", "payment"] = "credit"


class ConfirmTransactionResponse(BaseModel):
    transaction_id: int
    total_amount: Decimal
    updated_total_credit: Decimal
    created_at: datetime


 