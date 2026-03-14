# Credit Tracker Backend

Production-oriented FastAPI backend for credit tracking with Tamil voice-based transaction entry.

## Tech stack

- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- JWT authentication
- faster-whisper (Tamil speech-to-text)
- Ollama + `qwen3:8b` (Tamil text normalization + transaction parsing)
- rapidfuzz (fuzzy customer name matching)

## Features

- User auth with register/login and Bearer token
- Customer management
- Voice transaction preview pipeline:
   - audio transcription
   - Tamil text normalization
   - LLM transaction parsing
   - schema-level validation
   - fuzzy customer match
- Confirm transaction endpoint with safety checks before DB insert
- Rate limit for voice endpoint
- Audio upload validation (type + size)

## Project structure

Key modules:

- `api_server/main.py` - app creation, CORS, startup, health/root routes
- `api_server/api/v1/endpoints/auth.py` - auth APIs
- `api_server/api/v1/endpoints/customers.py` - customer APIs
- `api_server/api/v1/endpoints/voice.py` - voice preview pipeline
- `api_server/api/v1/endpoints/transactions.py` - confirm transaction API
- `api_server/services/whisper_service.py` - Tamil STT
- `api_server/services/text_normalizer.py` - LLM normalization
- `api_server/services/llm_parser.py` - LLM parser + fallbacks
- `api_server/services/tx_validator.py` - validation rules
- `api_server/services/customer_match.py` - fuzzy name matching

## Requirements

- Python 3.12
- PostgreSQL running and reachable from `DATABASE_URL`
- Ollama installed locally
- Ollama model pulled: `qwen3:8b`

## Environment variables

Copy `.env.example` to `.env` and update values.

Current variables:

```env
APP_NAME=Credit Tracker API
API_V1_PREFIX=/api/v1
ENVIRONMENT=development
SECRET_KEY=change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=60
ALGORITHM=HS256
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/credit_tracker
WHISPER_MODEL_SIZE=small
WHISPER_DEVICE=cpu
WHISPER_COMPUTE_TYPE=int8
VOICE_RATE_LIMIT=5/minute
MAX_AUDIO_SIZE_BYTES=5242880
```

## Local setup (Windows)

1. Install dependencies:

```powershell
cd backend
py -3.12 -m pip install -r requirements.txt
```

2. Configure environment:

```powershell
Copy-Item .env.example .env
```

3. Start Ollama service and pull model:

```powershell
C:\Users\Lenovo\AppData\Local\Programs\Ollama\ollama.exe pull qwen3:8b
```

4. Run backend:

```powershell
# From backend directory:
py -3.12 -m uvicorn api_server.main:app --host 127.0.0.1 --port 8000

# Or from project root:
py -3.12 -m uvicorn backend.api_server.main:app --host 127.0.0.1 --port 8000
```

## API URLs

- Base: `http://127.0.0.1:8000`
- Health: `GET /health`
- Docs (Swagger): `http://127.0.0.1:8000/docs`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`
- API prefix: `/api/v1`

## Authentication flow

1. Register:

`POST /api/v1/auth/register`

```json
{
   "username": "demo_shopkeeper",
   "password": "demoPassword123"
}
```

2. Login:

`POST /api/v1/auth/login`

3. Use returned token:

`Authorization: Bearer <access_token>`

## Endpoints

### Customers

- `GET /api/v1/customers`
- `POST /api/v1/customers`
- `GET /api/v1/customers/{customer_id}`

Create customer payload:

```json
{
   "name": "Kumar",
   "phone": "+919999999999"
}
```

### Voice preview

`POST /api/v1/voice-transaction`

Multipart form-data:

- `audio`: audio file
- `customer_id`: optional integer

Pipeline inside endpoint:

1. Transcribe Tamil audio (`faster-whisper`)
2. Normalize ASR Tamil text (Ollama `qwen3:8b`)
3. Parse transaction JSON (Ollama `qwen3:8b`)
4. Validate parsed output
5. Fuzzy-match customer name

Example response shape:

```json
{
   "transcription": "...",
   "normalized_text": "...",
   "parsed": {
      "name": "kumar",
      "item": "rice",
      "qty": 2,
      "amount": 120,
      "type": "purchase",
      "raw_text": "..."
   },
   "matched_customer_id": 3,
   "matched_customer_name": "Kumar",
   "is_valid": true,
   "items": [
      { "name": "rice", "qty": 2, "price": 120 }
   ],
   "calculated_total": 120,
   "parsing_warnings": []
}
```

### Confirm transaction

`POST /api/v1/confirm-transaction`

Supports two payload styles.

1. Existing item list flow:

```json
{
   "customer_id": 1,
   "items": [
      { "name": "rice", "qty": 2, "price": 120 }
   ]
}
```

2. Voice data flow:

```json
{
   "customer_id": 1,
   "voice_data": {
      "name": "kumar",
      "item": "rice",
      "qty": 2,
      "amount": 120,
      "type": "purchase",
      "raw_text": "குமார் அரிசி இரண்டு கிலோ 120 ரூபாய் வாங்கினார்"
   }
}
```

Safety checks before insert:

- transaction data valid
- customer exists
- amount > 0

## LLM parsing rules

Expected fields:

```json
{
   "name": "string | null",
   "item": "string | null",
   "qty": "int | null",
   "amount": "int | null",
   "type": "string | null",
   "raw_text": "string"
}
```

Rule mapping:

- Tamil number words -> digits
- `ரூபாய்` and similar -> amount extraction
- `கடன்` -> `loan`
- `கொடுத்தேன்` -> `paid`
- `வாங்கினார்` -> `purchase`
- default type -> `expense`

## Database behavior

- Tables are auto-created on startup with `Base.metadata.create_all(bind=engine)`.
- Confirm endpoint inserts into:
   - `transactions`
   - `transaction_items`
- Customer `total_credit` is updated inside a transaction-safe flow.

## Troubleshooting

### 1) `Cannot reach backend API. Start backend on http://127.0.0.1:8000`

Check:

- backend running on `127.0.0.1:8000`
- frontend using `NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1` (or default)
- hard refresh frontend after backend restart

### 2) `{"detail":"Not Found"}` on base URL

Use API paths with `/api/v1/*`. Root `/` is informational and not API prefix.

### 3) `ollama` command not recognized in VS Code terminal

Use full path:

```powershell
C:\Users\Lenovo\AppData\Local\Programs\Ollama\ollama.exe list
```

### 4) Parser not extracting correctly

- Ensure model is pulled: `qwen3:8b`
- First request can be slower due to model warm-up
- Try clear Tamil sentence for better extraction quality

### 5) Audio transcription failures

- Validate file type and size
- Check mic recording format
- Try clearer speech and less background noise

## Production notes

- Replace `SECRET_KEY` with a strong secret
- Use managed Postgres and secure credentials
- Put API behind reverse proxy/load balancer
- Enable structured logging and monitoring
- Add DB migrations (Alembic) before schema changes
- Consider async worker queue for long voice/LLM tasks
