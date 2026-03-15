from fastapi import HTTPException, UploadFile, status

ALLOWED_CONTENT_TYPES = {
    "audio/mpeg",
    "audio/mp3",
    "audio/wav",
    "audio/x-wav",
    "audio/wave",
    "audio/webm",
    "audio/mp4",
    "audio/m4a",
    "audio/aac",
    "audio/ogg",
    "audio/opus",
    "application/octet-stream",
}
ALLOWED_EXTENSIONS = {".mp3", ".wav", ".webm", ".m4a", ".mp4", ".ogg", ".oga", ".opus", ".aac"}


def validate_audio_upload(file: UploadFile, max_size: int, file_size: int) -> None:
    filename = (file.filename or "").lower()
    if not any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only supported audio formats are allowed (mp3/wav/webm/m4a/mp4/ogg/opus/aac)",
        )

    # Browsers may send parameters like "audio/webm;codecs=opus".
    normalized_content_type = (file.content_type or "").split(";", 1)[0].strip().lower()
    if normalized_content_type and normalized_content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported audio content-type")

    if file_size > max_size:
        limit_mb = max_size // (1024 * 1024)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Audio file exceeds {limit_mb}MB limit"
        )

# commit padding

# commit padding
 