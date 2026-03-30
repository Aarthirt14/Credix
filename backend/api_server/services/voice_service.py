from __future__ import annotations

import json
import re
from functools import lru_cache
from faster_whisper import WhisperModel

from api_server.core.config import get_settings


TYPE_ALIASES = {
    "loan": "loan",
    "credit": "loan",
    "paid": "paid",
    "payment": "paid",
    "purchase": "purchase",
    "expense": "expense",
}


def _extract_first_json(raw: str) -> dict | None:
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


def _fallback_amount_from_text(text: str) -> int:
    digit_match = re.search(r"\d+", text)
    if digit_match:
        return int(digit_match.group(0))

    from tamil_voice_system.number_parser import parse_tamil_number

    return parse_tamil_number(text)


def _normalize_type(value: object) -> str:
    raw = str(value or "").strip().lower()
    return TYPE_ALIASES.get(raw, "expense")


def _normalize_parsed_payload(parsed_data: dict | None, transcription: str) -> dict:
    parsed_data = parsed_data or {}
    normalized: dict = {
        "name": parsed_data.get("name") or None,
        "item": parsed_data.get("item") or None,
        "qty": parsed_data.get("qty") or 1,
        "amount": parsed_data.get("amount"),
        "type": _normalize_type(parsed_data.get("type")),
        "raw_text": transcription,
    }

    try:
        normalized["qty"] = int(normalized["qty"] or 1)
    except (TypeError, ValueError):
        normalized["qty"] = 1

    if normalized["qty"] <= 0:
        normalized["qty"] = 1

    try:
        normalized["amount"] = int(normalized["amount"])
    except (TypeError, ValueError):
        normalized["amount"] = _fallback_amount_from_text(transcription)

    if normalized["amount"] <= 0:
        normalized["amount"] = _fallback_amount_from_text(transcription)

    return normalized


@lru_cache(maxsize=1)
def get_whisper_model() -> WhisperModel:
    settings = get_settings()
    return WhisperModel(
        settings.WHISPER_MODEL_SIZE,
        device=settings.WHISPER_DEVICE,
        compute_type=settings.WHISPER_COMPUTE_TYPE,
    )


def transcribe_audio(file_path: str) -> str:
    """Old name for compatibility if needed."""
    return transcribe_tamil_audio(file_path)


def transcribe_tamil_audio(file_path: str) -> str:
    print(f"Pipeline: Transcribing audio file {file_path}...")
    try:
        model = get_whisper_model()
        segments, _ = model.transcribe(file_path, language="ta", beam_size=1)
        text = " ".join(segment.text.strip() for segment in segments if segment.text).strip()
        if not text:
            print("Pipeline: No speech detected.")
            raise RuntimeError("Speech not detected in the recording. Please speak clearly and try again.")
        print(f"Pipeline: Transcription complete ({len(text)} chars).")
        return text
    except RuntimeError:
        raise
    except Exception as exc:
        raise RuntimeError(f"Audio transcription failed: {exc}") from exc


def process_voice_transaction(file_path: str) -> dict:
    """
    Optimized Pipeline: Whisper (beam_size=1) -> Single-shot Ollama (Normalize + Parse)
    """
    transcription = transcribe_tamil_audio(file_path)
    
    # Single-shot prompt for both normalization and parsing
    combined_prompt = f"""
    You are an expert Tamil transaction parser. 
    1. Fix and normalize any errors in the following Tamil ASR text (names, amounts, item names).
    2. Extract transaction details into JSON.

    Input Text: "{transcription}"

    Instructions:
    - Identify names (e.g., Ravi, Kumar).
    - Identify amounts. Note: "அம்பது" is 50, "எண்பது" is 80. Be very careful with these similar sounding numbers.
    - Identify items and quantities (e.g., 4 kg).
    - Determine transaction type: "loan" (கடன்), "paid" (கொடுத்தார்/பெற்றேன்), "purchase", or "expense".

    Return JSON only:
    {{
      "normalized_text": "corrected tamil text",
      "parsed": {{
        "name": str | null,
        "item": str | null,
        "qty": int | null,
        "amount": int | null,
        "type": "loan" | "paid" | "purchase" | "expense",
        "raw_text": "{transcription}"
      }}
    }}
    """.strip()

    print("Pipeline: Starting single-shot Ollama request (Normalize + Parse)...")
    try:
        import ollama

        settings = get_settings()
        response = ollama.chat(
            model=settings.OLLAMA_MODEL,
            messages=[{"role": "user", "content": combined_prompt}],
            options={"temperature": 0},
            format="json",
        )
        raw_content = response["message"]["content"]
        result = _extract_first_json(raw_content) or {}
        parsed_payload = _normalize_parsed_payload(result.get("parsed"), transcription)

        return {
            "transcription": transcription,
            "normalized_text": str(result.get("normalized_text") or transcription),
            "parsed": parsed_payload,
        }
    except Exception:
        # Fallback to individual services if combined fails
        from api_server.services.text_normalizer import normalize_text
        from api_server.services.llm_parser import parse_transaction

        normalized = normalize_text(transcription)
        parsed = _normalize_parsed_payload(parse_transaction(normalized), transcription)
        return {
            "transcription": transcription,
            "normalized_text": normalized,
            "parsed": parsed,
        }



 