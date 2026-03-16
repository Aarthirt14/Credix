from __future__ import annotations


def validate_transaction(data: dict) -> bool:
    if not isinstance(data, dict):
        return False

    name = data.get("name")
    amount = data.get("amount")
    tx_type = data.get("type")

    if name is None or not str(name).strip():
        return False
    if tx_type is None or not str(tx_type).strip():
        return False

    try:
        amount_value = int(amount)
    except (TypeError, ValueError):
        return False

    return amount_value > 0


 