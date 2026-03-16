from __future__ import annotations

import ollama
from api_server.core.config import get_settings


NORMALIZER_PROMPT = (
    "You are a Tamil text normalizer. "
    "The input comes from speech recognition and may contain spelling mistakes or Romanized Tamil. "
    "Fix the sentence but keep meaning same. "
    "Fix Tamil number words, rupee words, and obvious names. "
    "Convert Romanized Tamil (like irubathu, aimpatu, roobai) to Tamil script if possible. "
    "Return only corrected sentence."
)

# Common Romanized Tamil to Tamil script mappings
ROMANIZED_TO_TAMIL = {
    'roobai': 'ரூபாய்',
    'rupai': 'ரூபாய்',
    'rubai': 'ரூபாய்',
    'irubathu': 'இருபது',
    'iruppathu': 'இருபது',
    'iruvathu': 'இருபது',
    'aimpatu': 'ஐம்பது',
    'aimbatu': 'ஐம்பது',
    'ambathu': 'அம்பது',
    'pathu': 'பத்து',
    'pathi': 'பத்து',
    'nooru': 'நூறு',
    'nuru': 'நூறு',
    'ravi': 'ராவி',
    'kumar': 'குமார்',
    'kavi': 'கவி',
    'vani': 'வாணி',
    'lakshmi': 'லட்சுமி',
}

def _transliterate_romanized_tamil(text: str) -> str:
    """Convert common Romanized Tamil words to Tamil script."""
    if not text:
        return text
    
    result = text
    for roman_word, tamil_word in ROMANIZED_TO_TAMIL.items():
        # Case-insensitive replacement
        import re
        result = re.sub(rf'\b{roman_word}\b', tamil_word, result, flags=re.IGNORECASE)
    
    return result

def normalize_text(text: str) -> str:
    if not text or not text.strip():
        return ""

    try:
        # First, try to transliterate Romanized Tamil to Tamil script
        pretransliterated = _transliterate_romanized_tamil(text.strip())
        
        settings = get_settings()
        response = ollama.chat(
            model=settings.OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": NORMALIZER_PROMPT},
                {"role": "user", "content": pretransliterated},
            ],
            options={"temperature": 0},
        )
        normalized = response["message"]["content"].strip()
        return normalized or text.strip()
    except Exception as exc:
        raise RuntimeError(f"Text normalization failed: {exc}") from exc



 