from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api_server.api.deps import get_current_user
from api_server.db.session import get_db
from api_server.models.customer import Customer
from api_server.models.transaction import Transaction, TransactionItem
from api_server.models.user import User
from api_server.schemas.transaction import ConfirmTransactionRequest, ConfirmTransactionResponse
from api_server.services.customer_match import match_customer
from api_server.services.tx_validator import validate_transaction

router = APIRouter()


@router.post("/confirm-transaction", response_model=ConfirmTransactionResponse)
def confirm_transaction(
    payload: ConfirmTransactionRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    customer = None
    tx_item_name = None
    tx_qty = None
    tx_type = None
    tx_raw_text = None

    if payload.voice_data:
        if not validate_transaction(payload.voice_data):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid voice transaction data")

        customer_id = payload.customer_id
        if customer_id is None:
            customers = db.query(Customer).all()
            matched_name = match_customer(str(payload.voice_data.get("name") or ""), customers)
            matched_customer = next((c for c in customers if c.name == matched_name), None)
            customer_id = matched_customer.id if matched_customer else None

        if customer_id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

        customer = db.query(Customer).filter(Customer.id == customer_id).with_for_update().first()
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

        amount = int(payload.voice_data.get("amount") or 0)
        if amount <= 0:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Amount must be greater than zero")

        total_amount = Decimal(str(amount))
        tx_item_name = str(payload.voice_data.get("item") or "Credit Entry")
        tx_qty = Decimal(str(payload.voice_data.get("qty") or 1))
        tx_type = str(payload.voice_data.get("type") or "expense")
        tx_raw_text = str(payload.voice_data.get("raw_text") or "")
    else:
        if payload.customer_id is None:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="customer_id is required")

        customer = db.query(Customer).filter(Customer.id == payload.customer_id).with_for_update().first()
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

        if not payload.items:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="items cannot be empty")

        total_amount = sum((item.price for item in payload.items), start=Decimal("0"))

        first_item = payload.items[0]
        tx_item_name = first_item.name
        tx_qty = first_item.qty
        tx_type = "expense"
        tx_raw_text = ""

    if total_amount <= 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Amount must be greater than zero")

    try:
        with db.begin_nested():
            transaction = Transaction(
                customer_id=customer.id,
                total_amount=total_amount,
                amount=total_amount,
                item=tx_item_name,
                qty=tx_qty,
                tx_type=tx_type,
                raw_text=tx_raw_text,
            )
            db.add(transaction)
            db.flush()

            if payload.voice_data:
                db.add(
                    TransactionItem(
                        transaction_id=transaction.id,
                        item_name=tx_item_name,
                        quantity=tx_qty,
                        price=total_amount,
                    )
                )
            else:
                for item in payload.items:
                    db.add(
                        TransactionItem(
                            transaction_id=transaction.id,
                            item_name=item.name,
                            quantity=item.qty,
                            price=item.price,
                        )
                    )

            customer.total_credit = Decimal(customer.total_credit) + total_amount
            db.add(customer)

        db.commit()
        db.refresh(transaction)
        db.refresh(customer)
        return ConfirmTransactionResponse(
            transaction_id=transaction.id,
            total_amount=transaction.total_amount,
            updated_total_credit=customer.total_credit,
            created_at=transaction.created_at,
        )
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Transaction failed") from exc


# commit padding

# commit padding
 