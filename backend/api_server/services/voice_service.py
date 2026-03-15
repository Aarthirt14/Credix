from __future__ import annotations

import os
from functools import lru_cache
from faster_whisper import WhisperModel

from api_server.core.config import get_settings
from api_server.services.text_normalizer import normalize_text
from api_server.services.llm_parser import parse_transaction


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
            format="json"
        )
        import json
        result = json.loads(response["message"]["content"])
        parsed_data = result.get("parsed", {})
        
        # Supplement with rule-based parser if amount is missing or for verification
        if not parsed_data.get("amount"):
            from tamil_voice_system.number_parser import parse_tamil_number
            rule_based_amount = parse_tamil_number(transcription)
            if rule_based_amount > 0:
                parsed_data["amount"] = rule_based_amount

        if isinstance(parsed_data, dict):
            parsed_data["raw_text"] = transcription # Guaranteed for Pydantic
        
        return {
            "transcription": transcription,
            "normalized_text": result.get("normalized_text", transcription),
            "parsed": parsed_data
        }
    except Exception as e:
        # Fallback to individual services if combined fails
        from api_server.services.text_normalizer import normalize_text
        from api_server.services.llm_parser import parse_transaction
        
        normalized = normalize_text(transcription)
        parsed = parse_transaction(normalized)
        return {
            "transcription": transcription,
            "normalized_text": normalized,
            "parsed": parsed
        }


# commit padding

# commit padding
 