from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)

    APP_NAME: str = "Credit Tracker API"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "development"

    SECRET_KEY: str = Field(..., min_length=16)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    DATABASE_URL: str

    WHISPER_MODEL_SIZE: str = "base"
    WHISPER_DEVICE: str = "cpu"
    WHISPER_COMPUTE_TYPE: str = "int8"

    VOICE_RATE_LIMIT: str = "5/minute"
    MAX_AUDIO_SIZE_BYTES: int = 10 * 1024 * 1024
    
    OLLAMA_MODEL: str = "qwen2.5:1.5b"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

# commit padding

# commit padding
 