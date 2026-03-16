from decimal import Decimal

from pydantic import BaseModel


class VoiceItemPreview(BaseModel):
    name: str
    qty: Decimal
    price: Decimal


class ParsedTransaction(BaseModel):
    name: str | None = None
    item: str | None = None
    qty: int | None = None
    amount: int | None = None
    type: str | None = None
    raw_text: str


class VoiceTransactionPreview(BaseModel):
    transcription: str
    normalized_text: str
    parsed: ParsedTransaction
    matched_customer_id: int | None = None
    matched_customer_name: str | None = None
    is_valid: bool
    items: list[VoiceItemPreview]
    calculated_total: Decimal
    parsing_warnings: list[str] = []


 