# Tamil Voice Transaction Parsing Guide

## Overview
This guide explains how the voice transaction parsing system works, from audio input to structured transaction data.

## Pipeline Architecture

### 1. Audio Transcription (Whisper)
- Uses faster-whisper for Tamil language transcription
- Model size: small (configurable)
- Beam size: 1 (for performance)
- Outputs: Tamil text with possible speech recognition errors

### 2. Text Normalization (Ollama)
- Pre-processing: Transliterate Romanized Tamil to script
- LLM-based normalization using Ollama
- Fixes common speech errors while preserving meaning
- Maps colloquial forms to formal Tamil

### 3. Transaction Parsing
- Dual-engine approach:
  - **LLM Parser**: Uses Ollama to extract structured JSON
  - **Fallback Rule-based Parser**: Tamil number parser + fuzzy matching
- Extracts: name, amount, item, quantity, transaction type

### 4. Customer Matching
- Fuzzy matches extracted customer name to database
- Handles name variations and speech errors
- Returns best matching customer or null

## Supported Number Formats

### Tamil Script Numbers
- Units: ஒன்று(1), இரண்டு(2), மூன்று(3), ... ஒன்பது(9)
- Tens: பத்து(10), பதி(10), இருபது(20), ..., தொண்ணூறு(90)
- Hundreds: நூறு(100), இருநூறு(200), ..., தொள்ளாயிரம்(900)
- Thousands: ஆயிரம்(1000), இரண்டாயிரம்(2000), ..., ஐந்தாயிரம்(5000)

### Romanized Tamil (Colloquial)
- Units: onnu(1), irandu(2), moonu(3), naalu(4), etc.
- Tens: irubathu(20), aimpatu(50), pathu(10), muppatu(30), etc.
- Hundreds: nooru(100), irunnooru(200), munnooru(300), etc.
- Examples: "ravi irubathu roobai" → Ravi, ₹20

### English Numerals (Direct)
- Plain digits: "20", "100", "500", etc.
- With currency: "20 rupees", "100 rs", etc.

## Fuzzy Matching

The parser uses rapidfuzz library for tolerance of speech variations:
- Similarity threshold: 85% (default), 70% (aggressive fallback)
- Handles: spelling errors, truncation, sound-alike words
- Example: "ஐம்பதி" matches "ஐம்பது" (20)

## Example Flows

### Flow 1: Pure Tamil
```
Input: "ராவி ஐம்பது ரூபாய் கடன்"
→ Name: ராவி (Ravi)
→ Amount: ஐம்பது (50)
→ Type: கடன் (loan)
→ Output: {name: "Ravi", amount: 50, type: "loan"}
```

### Flow 2: Romanized Tamil (Common)
```
Input: "ravi irubathu roobai"
→ Pre-process: ராவி இருபது ரூபாய்
→ Name: ராவி (Ravi)
→ Amount: இருபது (20)
→ Type: expense (default)
→ Output: {name: "Ravi", amount: 20, type: "expense"}
```

### Flow 3: Mixed with Speech Errors
```
Input: "அன்றாவி, எடுவது ரோ வாய்வில்லை" (garbled)
→ LLM normalization fixes to closest meaning
→ Rule-based parser extracts available amounts
→ Fallback matching for customer
```

## Configuration

Set environment variables in `.env`:
```
WHISPER_MODEL_SIZE=small
WHISPER_DEVICE=cpu
OLLAMA_MODEL=mistral
API_V1_PREFIX=/api/v1
VOICE_RATE_LIMIT=10/minute
```

## Testing

Test the parser:
```bash
cd backend
python tamil_voice_system/number_parser.py
python -m pytest test_pipeline.py -v
```
