"""
Local development setup instructions and troubleshooting guide.
"""

# Development Setup

## Prerequisites
- Python 3.12.7 (for MediaPipe compatibility)
- Node.js 18+
- SQLite3
- Ollama (for LLM-based parsing)

## Backend Setup

1. **Create virtual environment:**
   ```bash
   cd backend
   python -3.12 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with local settings
   ```

4. **Start backend:**
   ```bash
   python -m uvicorn api_server.main:app --host 127.0.0.1 --port 8000
   ```

## Frontend Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start dev server:**
   ```bash
   npm run dev
   # Open http://localhost:3000
   ```

## Troubleshooting

### Issue: "mp.solutions not found" error
**Solution:** Ensure using Python 3.12.7, not 3.14+
```bash
py -3.12 -m py_compile backend/api_server/main.py
```

### Issue: "Cannot reach backend API"
**Solution:** 
1. Check if backend is running: `http://127.0.0.1:8000/health`
2. Verify CORS is enabled (check main.py)
3. Check port 8000 is not in use: `lsof -i :8000`

### Issue: "Whisper model not found"
**Solution:**
1. First run downloads the model (~150MB)
2. Check model cache: `~/.cache/huggingface/`
3. Manually download: `faster_whisper --model small`

### Issue: "Ollama connection failed"
**Solution:**
1. Start Ollama: `ollama serve`
2. Install model: `ollama pull mistral`
3. Verify: `http://127.0.0.1:11434/api/tags`

### Issue: "Voice not being transcribed"
**Solution:**
1. Check audio format (should be WebM or WAV)
2. Verify microphone permissions
3. Check audio levels are not too low
4. Test with `test_whisper.py`

## Running Tests

```bash
# Number parser tests
python backend/tamil_voice_system/number_parser.py

# Integration tests
pytest backend/test_number_parser_integration.py -v

# Voice endpoint tests
pytest backend/test_voice_endpoint.py -v

# Performance benchmarks  
python backend/benchmark_parser.py
```

## Development Tips

1. **Clear voice cache:** `rm -rf ~/.cache/huggingface/`
2. **Check backend logs:** Add `--log-level debug` to uvicorn
3. **Debug parser:** Edit `test_debug_parsing.py` with test case
4. **Profile parser:** Use `benchmark_parser.py` script
5. **Monitor requests:** Add print statements in `voice_service.py`

## Performance Notes

- Whisper transcription: ~2-5 seconds for 10-second audio
- Ollama LLM parsing: ~1-2 seconds
- Total latency: ~3-7 seconds (depends on system)
- Use `--compute_type int8` for faster inference

## Database

- Default: SQLite at `./credit_tracker.db`
- For production: Configure PostgreSQL in `.env`
- Run migrations: `python -m alembic upgrade head`
