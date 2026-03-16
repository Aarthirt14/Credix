"""
Architecture and design decisions for the voice transaction system.
"""

# Architecture Design

## Overview

```
┌─────────────────────────────────────────────────────┐
│            Frontend (Next.js, React)                │
│   (Voice Recording & Transaction Preview UI)        │
└────────────────┬────────────────────────────────────┘
                 │ HTTP/Form-Data
                 ▼
┌─────────────────────────────────────────────────────┐
│         Voice API Endpoint                          │
│  (Audio Upload & Validation)                        │
└────────────────┬────────────────────────────────────┘
                 │ Audio File
                 ▼
┌─────────────────────────────────────────────────────┐
│  TRANSCRIPTION LAYER                                │
│  (Whisper - faster_whisper)                        │
│  ├─ Language: Tamil                                 │
│  ├─ Model size: small                               │
│  └─ Output: Tamil text (potentially with errors)    │
└────────────────┬────────────────────────────────────┘
                 │ Tamil text
                 ▼
┌─────────────────────────────────────────────────────┐
│  NORMALIZATION & PARSING LAYER                      │
│  ├─ Pre-process: Transliterate Romanized Tamil      │
│  ├─ LLM-based: Ollama (single-shot approach)        │
│  │   ├─ Fix speech errors                           │
│  │   ├─ Extract JSON (name, amount, type, etc.)     │
│  │   └─ Temperature: 0 (deterministic)              │
│  └─ Fallback: Rule-based Tamil number parser        │
│      ├─ Fuzzy matching (rapidfuzz)                  │
│      ├─ Composite number handling                   │
│      └─ Romanized Tamil support                     │
└────────────────┬────────────────────────────────────┘
                 │ Parsed: {name, amount, type, ...}
                 ▼
┌─────────────────────────────────────────────────────┐
│  CUSTOMER MATCHING LAYER                            │
│  ├─ Fuzzy match extracted name                      │
│  ├─ Return best matching customer                   │
│  └─ Handle speech variations                        │
└────────────────┬────────────────────────────────────┘
                 │ Matched customer ID
                 ▼
┌─────────────────────────────────────────────────────┐
│  RESPONSE: Transaction Preview                      │
│  ├─ Original transcription                          │
│  ├─ Normalized text                                 │
│  ├─ Parsed details                                  │
│  ├─ Item line items                                 │
│  ├─ Matched customer                                │
│  └─ Validity indicators & warnings                  │
└─────────────────────────────────────────────────────┘
```

## Key Design Decisions

### 1. Single-Shot LLM Pipeline
**Decision:** Combine text normalization and parsing in one Ollama call  
**Rationale:**
- Reduce API latency (2 calls → 1 call)
- Better context for LLM (sees both tasks together)
- Easier to handle failures (single fallback point)

### 2. Dual-Fallback Amount Extraction
**Decision:** Three-level strategy for amount extraction
1. Exact English numerals (regex)
2. Tamil number parser (rule-based)
3. Aggressive fuzzy matching

**Rationale:**
- Handles mixed language input (e.g., "20 rupees" or "irubathu roobai")
- Graceful degradation on parser failures
- Reliable amount extraction for core feature

### 3. Rule-Based Tamil Number Parser
**Decision:** Implement custom parser instead of relying purely on LLM  
**Rationale:**
- Faster (no LLM latency for number extraction)
- More reliable (consistent logic, no randomness)
- Handles compound numbers (200 + 50 + 5 = 255)
- Fuzzy matching for speech variations
- Romanized Tamil support for colloquial input

### 4. Pre-Transliteration Before LLM
**Decision:** Convert Romanized Tamil to Tamil script before LLM processing  
**Rationale:**
- LLM is trained primarily on Tamil script
- Improves normalization quality
- Handles common colloquial input patterns
- Example: "ravi irubathu roobai" → "ராவி இருபது ரூபாய்"

### 5. Composite Number Support
**Decision:** Sum components for multi-part numbers  
**Rationale:**
- Tamil number system uses composition (255 = நூற்று + ஐம்பத்து + ஐந்து)
- Users naturally speak in composed form ("இருநூற்று ஐம்பத்தி ஐந்து")
- Must handle both exact and fuzzy terms in composition

## Error Handling Strategy

```
Voice Input
    ↓
[Transcription] → Error? → Return "Speech not detected"
    ↓
[Pre-transliteration]
    ↓
[LLM Parsing] → Error? → Fall back to rule-based parser
    ↓
[Amount Extraction] 
  - Try English numerals
  - Try Tamil parser
  - Try fuzzy matching
    ↓
[Customer Matching]
    ↓
[Return Preview]
```

## Performance Optimizations

1. **Model Caching:** Whisper model cached with `@lru_cache(maxsize=1)`
2. **Lazy Regex Compilation:** Pattern compiled once in `__init__`
3. **Batched Fuzzy Matching:** Use token_set_ratio instead of ratio
4. **Early Exit:** Stop at first successful parse strategy

## Scalability Considerations

### Current Limitations
- Single Ollama instance (no load balancing)
- SQLite database (OK for development, not production)
- In-memory model caching (reasonable for single instance)

### Production Deployment
- Use PostgreSQL for transactions
- Load balance across Ollama instances
- Add Redis for response caching
- Implement request queuing for rate limiting
- Monitor model inference times

## Extension Points

1. **Add new languages:**
   - Update Whisper language parameter
   - Create language-specific number parser
   - Add language-specific normalization prompt

2. **Support additional input formats:**
   - Image OCR for handwritten amounts
   - Structured form input
   - Direct numeric keypad

3. **Improve matching:**
   - Train NER model for customer names
   - Add phonetic matching library
   - Implement spell-checker

4. **Enhance reliability:**
   - Add audio quality checks
   - Implement automatic retry with backoff
   - Add fallback to manual entry
