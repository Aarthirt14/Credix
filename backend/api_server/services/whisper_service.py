from __future__ import annotations

from functools import lru_cache

from faster_whisper import WhisperModel

from api_server.core.config import get_settings


@lru_cache(maxsize=1)
def get_whisper_model() -> WhisperModel:
    settings = get_settings()
    return WhisperModel(
        settings.WHISPER_MODEL_SIZE,
        device=settings.WHISPER_DEVICE,
        compute_type=settings.WHISPER_COMPUTE_TYPE,
    )


def transcribe_audio(file_path: str) -> str:
    try:
        model = get_whisper_model()
        segments, _ = model.transcribe(file_path, language="ta", beam_size=5)
        text = " ".join(segment.text.strip() for segment in segments if segment.text).strip()
        if not text:
            raise RuntimeError("Speech not detected in the recording. Please speak clearly and try again.")
        return text
    except RuntimeError:
        raise
    except Exception as exc:
        raise RuntimeError(f"Audio transcription failed: {exc}") from exc

