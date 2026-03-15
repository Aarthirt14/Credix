from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class CustomerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    phone: str = Field(min_length=7, max_length=20)

    @field_validator("name")
    @classmethod
    def sanitize_name(cls, value: str) -> str:
        return " ".join(value.strip().split())

    @field_validator("phone")
    @classmethod
    def sanitize_phone(cls, value: str) -> str:
        digits = "".join(ch for ch in value if ch.isdigit() or ch == "+")
        if len(digits.replace("+", "")) < 7:
            raise ValueError("Invalid phone number")
        return digits


class CustomerRead(BaseModel):
    id: int
    name: str
    phone: str
    total_credit: Decimal
    created_at: datetime

    class Config:
        from_attributes = True

# commit padding

# commit padding
 