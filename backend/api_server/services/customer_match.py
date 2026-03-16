from __future__ import annotations

from rapidfuzz import fuzz, process


def match_customer(name: str, customers: list) -> str:
    if not name or not str(name).strip() or not customers:
        return ""

    choices: list[str] = []
    for customer in customers:
        if isinstance(customer, str):
            choices.append(customer)
        else:
            customer_name = getattr(customer, "name", "")
            if customer_name:
                choices.append(str(customer_name))

    if not choices:
        return ""

    result = process.extractOne(str(name).strip(), choices, scorer=fuzz.WRatio)
    if not result:
        return ""

    best_match, score, _ = result
    return best_match if score >= 60 else ""


 