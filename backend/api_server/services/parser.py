from __future__ import annotations

import re
from difflib import SequenceMatcher
from decimal import Decimal

from api_server.schemas.transaction import ItemInput

NUMBER_WORDS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "ஒன்று": 1,
    "ஒரு": 1,
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
    "அய்ம்பது": 50,
    "அயமபது": 50,
    "அயமபத": 50,
    "அம்பது": 50,
    "aimbathu": 50,
    "ambathu": 50,
    "அறுபது": 60,
    "எழுபது": 70,
    "எண்பது": 80,
    "தொண்ணூறு": 90,
    "நூறு": 100,
    "ஐம்பத்தைந்து": 55,
    "அய்ம்பத்தைந்து": 55,
    "அம்பத்தைந்து": 55,
    "ஐம்பத்திஐந்து": 55,
    "ஐயமத்தையையுந்து": 55,
    "ஐயமததயயநத": 55,
    "aiyamathaiyaiundhu": 55,
    "aimbathainthu": 55,
    "aimpathainthu": 55,
    "ambathainthu": 55,
}

SEPARATORS = r",|\band\b|\bமற்றும்\b|\bபிறகு\b|\bthen\b"
UNIT_PATTERN = r"(?:kilo|kg|கிலோ|கிளோ|கிலோவு|லிட்டர்|litre|liter|packet|pack|பாக்கெட்|கிராம்|gram)?"
PRICE_SUFFIX = r"(?:rupai|rupaai|rupees|rs|ரூபாய்|ரூபாயி|ரூபா|ருபாய்|ருபாயி|ருவாயி|ருவாய்|ரூவாய்|ரபய|ரபாய்)"


class ParseResult:
    def __init__(self, items: list[ItemInput], warnings: list[str]):
        self.items = items
        self.warnings = warnings


def _normalize_numbers(text: str) -> str:
    lowered = text.lower()
    for word, number in NUMBER_WORDS.items():
        lowered = re.sub(rf"\b{re.escape(word)}\b", str(number), lowered)

    def _normalize_word_match(match: re.Match[str]) -> str:
        token = match.group(0)
        if token.isdigit():
            return token

        # Handle ASR variants such as "ஐயமத்தையையுந்து" by choosing the closest known number word.
        best_word = ""
        best_score = 0.0
        for candidate in NUMBER_WORDS:
            score = SequenceMatcher(None, token, candidate).ratio()
            if score > best_score:
                best_score = score
                best_word = candidate

        if best_word and best_score >= 0.72:
            return str(NUMBER_WORDS[best_word])
        return token

    return re.sub(r"[\w\u0B80-\u0BFF]+", _normalize_word_match, lowered)


def parse_tamil_transaction_text(text: str) -> ParseResult:
    normalized = _normalize_numbers(text)
    segments = [seg.strip() for seg in re.split(SEPARATORS, normalized, flags=re.IGNORECASE) if seg.strip()]

    items: list[ItemInput] = []
    warnings: list[str] = []

    # Strict pattern: quantity, unit, item name, price
    strict_pattern = re.compile(
        rf"(?P<qty>\d+(?:\.\d+)?)\s*{UNIT_PATTERN}\s*(?P<item>[a-zA-Z\u0B80-\u0BFF\s]+?)\s*(?P<price>\d+(?:\.\d+)?)\s*{PRICE_SUFFIX}",
        flags=re.IGNORECASE,
    )

    # Common spoken order in Tamil: item first, then quantity and price.
    item_first_pattern = re.compile(
        rf"(?P<item>[a-zA-Z\u0B80-\u0BFF\s]+?)\s+(?P<qty>\d+(?:\.\d+)?)\s*{UNIT_PATTERN}\s*(?P<price>\d+(?:\.\d+)?)\s*{PRICE_SUFFIX}",
        flags=re.IGNORECASE,
    )
    
    # Loose pattern: just look for a number followed by a price suffix or just a number at the end
    # Specifically handling cases like "குமார் இறுவேது ருவாயி" (Kumar 20 rupees)
    loose_price_pattern = re.compile(
        rf"(?P<price>\d+(?:\.\d+)?)(?:\s*{PRICE_SUFFIX})?",
        flags=re.IGNORECASE,
    )

    for segment in segments:
        strict_matches = list(strict_pattern.finditer(segment))
        if strict_matches:
            for match in strict_matches:
                item_name = " ".join(match.group("item").split()).strip()
                if len(item_name) < 3:
                    item_name = "Credit Entry"
                if item_name:
                    items.append(
                        ItemInput(
                            name=item_name,
                            qty=Decimal(match.group("qty")),
                            price=Decimal(match.group("price")),
                        )
                    )
            continue

        item_first_matches = list(item_first_pattern.finditer(segment))
        if item_first_matches:
            for match in item_first_matches:
                item_name = " ".join(match.group("item").split()).strip()
                if len(item_name) < 3:
                    item_name = "Credit Entry"
                if item_name:
                    items.append(
                        ItemInput(
                            name=item_name,
                            qty=Decimal(match.group("qty")),
                            price=Decimal(match.group("price")),
                        )
                    )
            continue
            
        # Fallback to loose extraction if strict pattern fails
        price_matches = list(loose_price_pattern.finditer(segment))
        if price_matches:
            # Take the last number found as the price, as amounts are usually at the end
            last_match = price_matches[-1]
            price_val = last_match.group("price")
            
            # Use the rest of the segment as the item name, or a default
            item_name = segment.replace(last_match.group(0), "").strip()
            if not item_name:
                item_name = "Credit Entry"
            elif len(item_name) < 3:
                item_name = "Credit Entry"
                
            items.append(
                ItemInput(
                    name=item_name,
                    qty=Decimal("1"),
                    price=Decimal(price_val),
                )
            )
        else:
            warnings.append(f"Unable to parse segment: '{segment}'")

    return ParseResult(items=items, warnings=warnings)



 