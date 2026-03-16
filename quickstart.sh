#!/bin/bash
# Quick start script for developer setup

set -e

echo "═══════════════════════════════════════════════════════"
echo "  Tamil Voice Credit Tracker - Quick Start Setup"
echo "═══════════════════════════════════════════════════════"
echo ""

# Check Python version
echo "📦 Checking Python version..."
if ! command -v python3.12 &> /dev/null; then
  echo "❌ Python 3.12 is required. Found:"
  python3 --version
  exit 1
fi
echo "✓ Python 3.12 found"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
cd backend
python3.12 -m venv venv
source venv/bin/activate
echo "✓ Virtual environment created"
echo ""

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Create environment file
echo "📦 Setting up environment..."
if [ ! -f .env ]; then
  echo "SECRET_KEY=dev-secret-key-change-in-prod" > .env
  echo "DATABASE_URL=sqlite:///./credit_tracker.db" >> .env
  echo "DEBUG=True" >> .env
  echo "✓ .env created with defaults"
else
  echo "✓ .env already exists"
fi
echo ""

# Go back to root
cd ..

# Setup frontend
echo "📦 Installing Node dependencies..."
npm install > /dev/null 2>&1
echo "✓ Node dependencies installed"
echo ""

echo "═══════════════════════════════════════════════════════"
echo "  Setup complete! Ready to start development"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "To start development:"
echo "  Terminal 1 (Backend):"
echo "    cd backend"
echo "    source venv/bin/activate"
echo "    python -m uvicorn api_server.main:app --reload"
echo ""
echo "  Terminal 2 (Frontend):"
echo "    npm run dev"
echo ""
echo "Then open: http://localhost:3000"
echo ""
