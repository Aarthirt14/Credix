from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from api_server.api.v1.router import api_router
from api_server.core.config import get_settings
from api_server.core.rate_limiter import limiter
from api_server.db.base import Base
from api_server.db.session import engine
from api_server.services.voice_service import get_whisper_model

settings = get_settings()

app = FastAPI(title=settings.APP_NAME)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    print("Startup: Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Startup: Pre-loading Whisper model...")
    try:
        get_whisper_model()
        print("Startup: Whisper model ready.")
    except Exception as e:
        print(f"Startup: Error pre-loading Whisper model: {e}")


@app.get("/")
def root() -> dict[str, str]:
    return {
        "app": settings.APP_NAME,
        "status": "ok",
        "docs": "/docs",
        "openapi": "/openapi.json",
        "api_base": settings.API_V1_PREFIX,
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.middleware("http")
async def add_rate_limit_headers(request: Request, call_next):
    response = await call_next(request)
    return response


app.include_router(api_router, prefix=settings.API_V1_PREFIX)


 