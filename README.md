# 🎙️ Tamil Voice Credit Tracker

A modern, full-stack application for tracking customer credit transactions using voice input in Tamil. Built with Next.js, FastAPI, and advanced AI/ML models for voice recognition and natural language processing.

## ✨ Features

### Voice Processing
- **Real-time Speech Recognition**: Whisper-based Tamil language transcription
- **Intelligent Parsing**: LLM-powered extraction of transaction details from natural speech
- **Smart Fallback**: Multi-strategy number parsing with fuzzy matching for speech variations
- **Romanized Tamil Support**: Handles colloquial Romanized input (e.g., "irubathu" for 20)

### Transaction Management  
- **Quick Entry**: Record credit transactions via voice in seconds
- **Customer Linking**: Automatic customer name matching with fuzzy search
- **Amount Validation**: Real-time amount verification before confirmation
- **Real-time Dashboard**: Live balance tracking and transaction history

### Advanced Features
- **Rate Limiting**: Per-user API rate limits (10 transactions/min)
- **Multi-user Support**: SQLAlchemy ORM with database session management
- **Mobile Responsive**: Works seamlessly on desktop and mobile devices
- **Dark Mode**: Full dark theme support with Tailwind CSS

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

**Windows:**
```powershell
powershell .\quickstart.ps1
```

**Linux/Mac:**
```bash
bash quickstart.sh
```

### Option 2: Manual Setup

```bash
# 1. Create Python virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# 2. Install Python dependencies
pip install -r backend/requirements.txt

# 3. Set up environment
cp .env.example .env
# Edit .env with your configuration

# 4. Start backend (port 8000)
cd backend/api_server
python main.py

# 5. In a new terminal, start frontend (port 3000)
npm install
npm run dev
```

**Visit:** 
- Frontend: http://localhost:3000
- Backend API: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8000/docs

## 📋 Requirements

### System Requirements
- **Python**: 3.12.7 (MediaPipe compatibility)
- **Node.js**: 18+ (for frontend)
- **RAM**: 4GB minimum (8GB recommended for ML models)
- **Disk Space**: 5GB for models

### Dependencies
- **Frontend**: Next.js 16.1.6, React 19.2.4, TypeScript, Tailwind CSS
- **Backend**: FastAPI 0.115.6, SQLAlchemy 2.0.37, faster-whisper
- **ML**: Ollama (for LLM), Whisper (transcription)
- **Database**: SQLite (dev), PostgreSQL (production)

### External Services
- **Ollama**: For LLM-based text parsing
  - Download: https://ollama.ai
  - Model: `ollama pull mistral` (or same model)

## 🎯 Usage

### Voice Transaction Entry

1. Click **"Add Transaction"** button
2. Grant microphone permission (if not already granted)
3. Speak transaction details in Tamil:
   - Example: "ரவி இருபது ரூபாய்" (Ravi, 20 rupees)
   - Romanized: "ravi irubathu roobai"
4. Review parsed details in preview
5. Select customer and confirm

### Supported Number Formats

| Format | Example | Parses As |
|--------|---------|-----------|
| Tamil Script | ஐம்பது | 50 |
| Romanized | irubathu | 20 |
| English | 250 | 250 |
| Composite | "nooru irubathu" | 120 |
| Fuzzy Match | "ஐம்பது" (50) spoken as "[SPEECH VARIATION]" | 50 |

## 📁 Project Structure

```
credit/
├── app/                    # Next.js app directory
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── globals.css        # Global styles
├── components/            # React components
│   ├── ui/               # shadcn/ui components
│   ├── dashboard.tsx     # Main transaction list
│   ├── customer-detail.tsx
│   └── voice-overlay.tsx # Voice recording UI
├── lib/                  # Utilities
│   ├── api.ts           # API client
│   ├── i18n.ts          # i18n setup
│   └── utils.ts         # Helper functions
├── backend/             # FastAPI backend
│   ├── api_server/
│   │   ├── main.py      # FastAPI app
│   │   ├── api/         # API endpoints
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── services/    # Business logic
│   │   └── core/        # Config, security
│   └── tamil_voice_system/
│       ├── pipeline.py       # Voice pipeline
│       ├── number_parser.py  # Number parsing
│       └── downloader.py     # Model downloader
├── docs/                # Documentation
│   ├── VOICE_PARSING_GUIDE.md
│   ├── ARCHITECTURE.md
│   ├── DEVELOPMENT.md
│   ├── DEPLOYMENT.md
│   ├── API_INTEGRATION_GUIDE.md
│   └── CONTRIBUTING.md
├── FAQ.md              # Frequently asked questions
└── README.md           # This file
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ Frontend (Next.js 16.1 / React 19 / TypeScript)            │
│ • Voice recording UI with Web Audio API                    │
│ • Real-time transaction display with shadcn/ui components │
└────────────────────── HTTP ─────────────────────────────────┘
                           ↓↑
┌─────────────────────────────────────────────────────────────┐
│ Backend (FastAPI 0.115 / SQLAlchemy 2.0)                   │
│ • Rate limiting middleware                                  │
│ • CORS enabled for localhost:3000                           │
├─────────────────────────────────────────────────────────────┤
│ Voice Processing Pipeline (Services)                        │
│ 1. Whisper Transcription (faster-whisper)                   │
│ 2. Text Normalizer (via Ollama LLM)                        │
│ 3. LLM Parser (via Ollama) + Rule-based fallback           │
│ 4. Number Extractor (TamilNumberParser with fuzzy match)   │
└─────────────────────────────────────────────────────────────┘
                           ↓↑
┌─────────────────────────────────────────────────────────────┐
│ External Services                                           │
│ • Ollama: Text normalization & parsing (Mistral 7B)        │
│ • Whisper: Speech-to-text in Tamil (openai/whisper-base)   │
└─────────────────────────────────────────────────────────────┘
                           ↓↑
┌─────────────────────────────────────────────────────────────┐
│ Database (SQLite / PostgreSQL)                              │
│ • Users, Customers, Transactions, Items, Debts             │
└─────────────────────────────────────────────────────────────┘
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed design documentation.

## 📖 Documentation

- **[VOICE_PARSING_GUIDE.md](backend/VOICE_PARSING_GUIDE.md)** - How voice parsing works, supported formats
- **[API_INTEGRATION_GUIDE.md](backend/API_INTEGRATION_GUIDE.md)** - Voice endpoint documentation with examples
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design and decision rationale
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Development setup, debugging, performance tuning
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment with Docker, monitoring
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contributing guidelines and code style
- **[FAQ.md](FAQ.md)** - Frequently asked questions and troubleshooting

## 🧪 Testing

### Run Tests
```bash
cd backend
pytest test_number_parser_integration.py -v
```

### Run Benchmarks
```bash
python backend/benchmark_parser.py
```

### Test Voice Endpoint
```bash
curl -X POST http://127.0.0.1:8000/api/v1/voice-transaction \
  -F "file=@test_audio.wav" \
  -F "customer_id=1"
```

See [DEVELOPMENT.md](DEVELOPMENT.md#testing) for detailed testing documentation.

## ⚙️ Configuration

### Environment Variables
```env
# Backend
BACKEND_URL=http://127.0.0.1:8000
DATABASE_URL=sqlite:///credit_tracker.db
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
WHISPER_MODEL_SIZE=base
WHISPER_DEVICE=cpu
WHISPER_COMPUTE_TYPE=float32

# Frontend
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

See [DEVELOPMENT.md](DEVELOPMENT.md#configuration) for all available options.

## 🐛 Troubleshooting

### "Cannot reach backend API"
- Check if backend is running: `curl http://127.0.0.1:8000/health`
- Verify port 8000 is available
- Check firewall settings

### "Ollama not connected"
- Install Ollama: https://ollama.ai
- Start Ollama service
- Pull model: `ollama pull mistral`

### High CPU usage
- Use smaller Whisper model: `WHISPER_MODEL_SIZE=tiny`
- Enable GPU: `WHISPER_DEVICE=cuda`
- Use quantization: `WHISPER_COMPUTE_TYPE=int8`

See [FAQ.md](FAQ.md) for more troubleshooting steps.

## 📊 Performance

### Benchmark Results (on macOS M1)
```
Model Initialization: 2.3s
Tamil Script Parsing (20 items): 1.2ms avg
Romanized Tamil Parsing (15 items): 0.8ms avg
Fuzzy Matching (50 items): 0.5ms avg
End-to-End Voice Transaction: 4-7 seconds
```

See [DEVELOPMENT.md](DEVELOPMENT.md#performance-tuning) for optimization tips.

## 🔐 Security

- **Rate Limiting**: 10 transactions per minute per user
- **CORS**: Restricted to localhost:3000 in development
- **Input Validation**: Pydantic schemas with strict validation
- **SQL Injection**: Protected via SQLAlchemy ORM
- **Audio Privacy**: Audio files not persisted, only transcription stored

See [DEPLOYMENT.md](DEPLOYMENT.md#security-checklist) for production security guidelines.

## 🚀 Deployment

### Docker Deployment
```bash
# Build and run
docker-compose up --build

# Or individual services
docker build -t credit-tracker-backend backend/
docker build -t credit-tracker-frontend .
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Production configuration
- Database setup (PostgreSQL)
- Monitoring and logging
- Security checklist
- Backup and recovery

## 📈 Roadmap

### Planned Features
- [ ] Multilingual support (Telugu, Kannada, Bengali)
- [ ] Receipt/bill image parsing (OCR)
- [ ] SMS integration for transaction confirmations
- [ ] WhatsApp Business API integration
- [ ] Advanced analytics and reporting
- [ ] Mobile app (React Native)
- [ ] Offline support (IndexedDB + service workers)
- [ ] Payment processing (Razorpay, PhonePe)

See [ARCHITECTURE.md](ARCHITECTURE.md#scalability) for future expansion ideas.

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code style guidelines (PEP8, ESLint)
- Testing requirements
- Git commit format
- Pull request process

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## 💬 Support

- **Issues**: Open an issue on GitHub
- **Questions**: Check [FAQ.md](FAQ.md) first
- **Documentation**: See docs folder
- **Code Examples**: Check test files and API docs

## 🙏 Acknowledgments

- OpenAI's Whisper for speech recognition
- Meta's Faster Whisper for optimization
- Ollama for local LLM inference
- shadcn/ui for component library
- The open-source community

---

**Made with ❤️ for the Tamil business community**

Happy credit tracking! 🎉
