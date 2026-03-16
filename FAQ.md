# Frequently Asked Questions

## Installation & Setup

### Q: Which Python version should I use?
**A:** Python 3.12.7 is required for MediaPipe compatibility. Python 3.14+ may cause issues with `mp.solutions`. Use `py -3.12` on Windows.

### Q: How do I set up the development environment?
**A:** Run the quick start script:
- Linux/Mac: `bash quickstart.sh`
- Windows: `powershell .\quickstart.ps1`

### Q: Do I need Ollama to run the app?
**A:** Yes, Ollama is required for LLM-based text parsing. Install from https://ollama.ai then run `ollama pull mistral`.

### Q: Can I use the app without Ollama?
**A:** The system will fall back to rule-based number parsing if Ollama is unavailable, but functionality will be limited.

## Voice Parsing

### Q: What audio formats are supported?
**A:** WebM (preferred), WAV, MP3. The frontend records WebM format.

### Q: Why is my voice not being recognized?
**A:** 
1. Check microphone permissions
2. Speak clearly and at normal volume
3. Ensure 10-second minimum recording
4. Check audio quality (no extreme background noise)

### Q: Can I use a different language?
**A:** Currently Tamil only. The system can be extended for other languages by:
1. Changing Whisper language parameter
2. Creating language-specific number parser
3. Updating LLM prompt for that language

### Q: How accurate is the number extraction?
**A:** 
- Clean Tamil: 98%+ accuracy
- Romanized Tamil: 90%+ accuracy  
- Mixed/noisy input: 75-85% accuracy

## Backend Issues

### Q: "Cannot reach backend API" error
**A:** The backend must be running on port 8000. Check:
1. Is backend process running? (`curl http://127.0.0.1:8000/health`)
2. Is port 8000 available?
3. Check firewall settings
4. Verify CORS is enabled in main.py

### Q: High CPU usage from Whisper model
**A:** This is normal during transcription. To optimize:
1. Use smaller model: `WHISPER_MODEL_SIZE=tiny` in .env
2. Use GPU: `WHISPER_DEVICE=cuda`
3. Use quantization: `WHISPER_COMPUTE_TYPE=int8`

### Q: Database locked error
**A:** SQLite issue with multiple processes. Solutions:
1. Close other instances of the app
2. Delete `credit_tracker.db` to reset (dev only)
3. Switch to PostgreSQL for production

### Q: Rate limit exceeded error
**A:** The API allows 10 voice transactions per minute per user. Wait before submitting more.

## Data & Privacy

### Q: Where is data stored?
**A:** By default, SQLite database at `backend/credit_tracker.db`. Change in `.env` for other locations.

### Q: Is audio saved?
**A:** No, audio is transcribed and discarded immediately. Only transaction data is saved.

### Q: Can I export my data?
**A:** Use the API endpoints or access the SQLite database directly.

## Performance

### Q: Why is voice processing slow?
**A:** 
- Whisper transcription: 2-5 seconds
- LLM parsing: 1-2 seconds
- Total: 3-7 seconds typical

### Q: How can I improve performance?
**A:**
1. Use `WHISPER_COMPUTE_TYPE=int8` (faster, slightly less accurate)
2. Use smaller Whisper model (`tiny` or `base`)
3. Use GPU acceleration if available
4. Run Ollama on GPU: `ollama run mistral --gpu`

### Q: Can I run this on a low-end device?
**A:** With optimization:
1. Use `tiny` Whisper model
2. Use `int8` quantization
3. Use smaller LLM (non-Mistral option)
4. Reduce refresh rate

## Troubleshooting

### Q: Tests are failing
**A:** Run:
```bash
# Check Python version
python --version  # Should be 3.12.x

# Run specific test
pytest backend/test_number_parser_integration.py -v

# Check dependencies
pip list | grep -E "faster-whisper|ollama|rapidfuzz"
```

### Q: How do I debug the number parser?
**A:** Edit `backend/test_debug_parsing.py` with your test case and run:
```bash
python backend/test_debug_parsing.py
```

### Q: The app won't start - "port already in use"
**A:** Find and stop the process using port 8000:
```bash
# Linux/Mac
lsof -i :8000 | grep -v PID | awk '{print $2}' | xargs kill -9

# Windows PowerShell
Get-NetTCPConnection -LocalPort 8000 | Stop-Process
```

### Q: Frontend can't connect to backend  
**A:**
1. Check backend is running on port 8000
2. Check CORS is enabled (see main.py)
3. Ensure `API_BASE_URL` is correct in frontend config
4. Check firewall/network settings

## Contributing

### Q: How do I contribute?
**A:** See CONTRIBUTING.md for guidelines on:
- Code style
- Testing requirements
- Commit format
- PR process

### Q: What areas need improvement?
**A:** Check GitHub issues for:
- Performance optimization
- Multilingual support
- New features
- Bug fixes

## Getting Help

- Check this FAQ first
- Read DEVELOPMENT.md for detailed setup
- Search GitHub issues
- Check code comments and docstrings
- Review test files for usage examples
