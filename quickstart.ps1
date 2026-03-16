#!/bin/bash
# Windows PowerShell version of quickstart

Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Tamil Voice Credit Tracker - Quick Start Setup" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "📦 Checking Python version..." -ForegroundColor Yellow
$pythonCmd = Get-Command py -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
  Write-Host "❌ Python not found" -ForegroundColor Red
  exit 1
}
$version = & py --version
Write-Host "✓ Found: $version" -ForegroundColor Green
Write-Host ""

# Create virtual environment
Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
Push-Location backend
& py -3.12 -m venv venv
& .\venv\Scripts\Activate.ps1
Write-Host "✓ Virtual environment created" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Yellow
& pip install --upgrade pip
& pip install -r requirements.txt
Write-Host "✓ Dependencies installed" -ForegroundColor Green
Pop-Location
Write-Host ""

# Create environment file
Write-Host "📦 Setting up environment..." -ForegroundColor Yellow
if (-not (Test-Path backend\.env)) {
  @"
SECRET_KEY=dev-secret-key-change-in-prod
DATABASE_URL=sqlite:///./credit_tracker.db
DEBUG=True
"@ | Set-Content backend\.env -Encoding UTF8
  Write-Host "✓ .env created" -ForegroundColor Green
} else {
  Write-Host "✓ .env already exists" -ForegroundColor Green
}
Write-Host ""

# Setup frontend
Write-Host "📦 Installing Node dependencies..." -ForegroundColor Yellow
& npm install > $null 2>&1
Write-Host "✓ Node dependencies installed" -ForegroundColor Green
Write-Host ""

Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Setup complete! Ready to start development" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start development:" -ForegroundColor Yellow
Write-Host "  PowerShell Terminal 1 (Backend):" -ForegroundColor White
Write-Host "    cd backend" -ForegroundColor Gray
Write-Host "    .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "    python -m uvicorn api_server.main:app --reload" -ForegroundColor Gray
Write-Host ""
Write-Host "  PowerShell Terminal 2 (Frontend):" -ForegroundColor White
Write-Host "    npm run dev" -ForegroundColor Gray
Write-Host ""
Write-Host "Then open: http://localhost:3000" -ForegroundColor Green
