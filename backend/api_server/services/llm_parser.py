from __future__ import annotations

import json
import re

import ollama
from api_server.core.config import get_settings


PARSER_PROMPT = """
Extract transaction details from Tamil text.
Return JSON only with this exact schema:
{
  "name": str | null,
  "item": str | null,
  "qty": int | null,
  "amount": int | null,
  "type": str | null,
  "raw_text": str
}

Rules:
- Convert Tamil number words to digits (including Romanized forms like irubathu=20, aimpatu=50).
- If text contains ரூபாய் or rupees/roobai, map to amount.
- கடன் => loan
- கொடுத்தேன் => paid
- வாங்கினார் => purchase
- default type => expense
- raw_text must be input text as-is.
- Return JSON object only, no markdown.
""".strip()


NUMBER_WORDS = {
    "பூஜ்யம்": 0,
    "ஒரு": 1,
    "ஒன்று": 1,
    "இரண்டு": 2,
    "மூன்று": 3,
    "நான்கு": 4,
    "ஐந்து": 5,
    "ஆறு": 6,
    "ஏழு": 7,
    "எட்டு": 8,
    "ஒன்பது": 9,
    "பத்து": 10,
    "பதினொன்று": 11,
    "பன்னிரண்டு": 12,
    "பதிமூன்று": 13,
    "பதிநான்கு": 14,
    "பதினைந்து": 15,
    "பதினாறு": 16,
    "பதினேழு": 17,
    "பதினெட்டு": 18,
    "பத்தொன்பது": 19,
    "இருபது": 20,
    "முப்பது": 30,
    "நாற்பது": 40,
    "ஐம்பது": 50,
    "அம்பது": 50,
    "அறுபது": 60,
    "எழுபது": 70,
    "எண்பது": 80,
    "தொண்ணூறு": 90,
    "நூறு": 100,
}


def _default_payload(text: str) -> dict:
    return {
        "name": None,
        "item": None,
        "qty": None,
        "amount": None,
        "type": None,
        "raw_text": text,
    }


def _extract_json(raw: str) -> dict | None:
    if not raw:
        return None

    try:
        parsed = json.loads(raw)
        return parsed if isinstance(parsed, dict) else None
    except json.JSONDecodeError:
        pass

    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None

    try:
        parsed = json.loads(raw[start : end + 1])
        return parsed if isinstance(parsed, dict) else None
    except json.JSONDecodeError:
        return None


def _normalize_number_words(text: str) -> str:
    normalized = text
    for word, value in NUMBER_WORDS.items():
        normalized = re.sub(rf"\b{re.escape(word)}\b", str(value), normalized)
    return normalized


def _infer_type(text: str, current_type: str | None) -> str:
    if current_type and current_type.strip():
        return current_type.strip().lower()

    normalized = text.lower()
    if "கடன்" in text:
        return "loan"
    if "கொடுத்தேன்" in text:
        return "paid"
    if "வாங்கினார்" in text:
        return "purchase"
    return "expense"


def _infer_amount(text: str, current_amount: int | None) -> int | None:
    if isinstance(current_amount, int) and current_amount > 0:
        return current_amount

    # First, try to find English numerals
    match = re.search(r"(\d+)\s*(?:ரூபாய்|ருபாய்|rupees|rs)?", text, flags=re.IGNORECASE)
    if match:
        value = int(match.group(1))
        if value > 0:
            return value

    # Second, try to parse Tamil number words
    from tamil_voice_system.number_parser import parse_tamil_number
    try:
        tamil_amount = parse_tamil_number(text)
        if tamil_amount > 0:
            return tamil_amount
    except Exception:
        pass

    return None


def _to_int(value: object) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        token = value.strip()
        if token.isdigit():
            return int(token)
    return None


def parse_transaction(text: str) -> dict:
    normalized_text = _normalize_number_words(text.strip())
    payload = _default_payload(normalized_text)

    try:
        settings = get_settings()
        response = ollama.chat(
            model=settings.OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": PARSER_PROMPT},
                {"role": "user", "content": normalized_text},
            ],
            options={"temperature": 0},
            format="json",
        )
        raw_content = response["message"]["content"]
        llm_data = _extract_json(raw_content) or {}
    except Exception:
        llm_data = {}

    payload["name"] = llm_data.get("name")
    payload["item"] = llm_data.get("item")
    payload["qty"] = _to_int(llm_data.get("qty"))
    payload["amount"] = _to_int(llm_data.get("amount"))
    payload["type"] = llm_data.get("type")
    payload["raw_text"] = normalized_text

    payload["amount"] = _infer_amount(normalized_text, payload["amount"])
    payload["type"] = _infer_type(normalized_text, payload["type"])

    if payload["qty"] is not None and payload["qty"] <= 0:
        payload["qty"] = None
    if payload["amount"] is not None and payload["amount"] <= 0:
        payload["amount"] = None

    if payload["item"] is not None:
        payload["item"] = str(payload["item"]).strip() or None
    if payload["name"] is not None:
        payload["name"] = str(payload["name"]).strip() or None

    return payload



 