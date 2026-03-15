import os
import tempfile
from decimal import Decimal

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile, status
from sqlalchemy.orm import Session

from api_server.api.deps import get_current_user
from api_server.core.config import get_settings
from api_server.core.rate_limiter import limiter
from api_server.db.session import get_db
from api_server.models.customer import Customer
from api_server.models.user import User
from api_server.schemas.voice import ParsedTransaction, VoiceItemPreview, VoiceTransactionPreview
from api_server.services.customer_match import match_customer
from api_server.services.voice_service import process_voice_transaction
from api_server.services.tx_validator import validate_transaction
from api_server.utils.file_validation import validate_audio_upload

router = APIRouter()


@router.post("/voice-transaction", response_model=VoiceTransactionPreview)
@limiter.limit(get_settings().VOICE_RATE_LIMIT)
def voice_transaction_preview(
    request: Request,
    customer_id: int | None = Form(default=None),
    audio: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    _ = request
    settings = get_settings()

    selected_customer = None
    if customer_id is not None:
        selected_customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not selected_customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    audio_bytes = audio.file.read()
    file_size = len(audio_bytes)
    validate_audio_upload(audio, settings.MAX_AUDIO_SIZE_BYTES, file_size)

    suffix = os.path.splitext(audio.filename or "")[1] or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(audio_bytes)
        temp_path = temp_file.name

    try:
        pipeline_result = process_voice_transaction(temp_path)
        transcription = pipeline_result["transcription"]
        normalized_text = pipeline_result["normalized_text"]
        parsed = pipeline_result["parsed"]
        
        tx_valid = validate_transaction(parsed)

        customers = db.query(Customer).all()
        matched_name = match_customer(parsed.get("name") or "", customers)
        matched_customer = next((c for c in customers if c.name == matched_name), None)

        if selected_customer is not None:
            matched_customer = selected_customer
            matched_name = selected_customer.name

        amount_value = parsed.get("amount")
        qty_value = parsed.get("qty") or 1
        item_value = parsed.get("item") or "Credit Entry"

        total = Decimal(str(amount_value or 0))
        items = []
        if amount_value and amount_value > 0:
            items = [
                VoiceItemPreview(
                    name=item_value,
                    qty=Decimal(str(qty_value)),
                    price=Decimal(str(amount_value)),
                )
            ]

        return VoiceTransactionPreview(
            transcription=transcription,
            normalized_text=normalized_text,
            parsed=ParsedTransaction(**parsed),
            matched_customer_id=matched_customer.id if matched_customer else None,
            matched_customer_name=matched_name or None,
            is_valid=tx_valid,
            items=items,
            calculated_total=total,
            parsing_warnings=[] if tx_valid else ["Unable to fully validate parsed transaction"],
        )
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


# commit padding

# commit padding
 