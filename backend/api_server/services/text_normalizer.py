from __future__ import annotations

import ollama
from api_server.core.config import get_settings


NORMALIZER_PROMPT = (
    "You are a Tamil text normalizer. "
    "The input comes from speech recognition and may contain spelling mistakes. "
    "Fix the sentence but keep meaning same. "
    "Fix Tamil number words, rupee words, and obvious names. "
    "Return only corrected sentence."
)


def normalize_text(text: str) -> str:
    if not text or not text.strip():
        return ""

    try:
        settings = get_settings()
        response = ollama.chat(
            model=settings.OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": NORMALIZER_PROMPT},
                {"role": "user", "content": text.strip()},
            ],
            options={"temperature": 0},
        )
        normalized = response["message"]["content"].strip()
        return normalized or text.strip()
    except Exception as exc:
        raise RuntimeError(f"Text normalization failed: {exc}") from exc

