# HealFind AI - PowerShell Startup Script
Write-Host "🏥 HealFind AI - Starting Application..." -ForegroundColor Green
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>$null
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed or not in PATH!" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "⚡ Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Install requirements
Write-Host "📥 Installing requirements..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create templates directory and copy HTML file
if (-not (Test-Path "templates")) {
    New-Item -ItemType Directory -Path "templates"
}
Copy-Item "index.html" "templates\" -Force

# Start the application
Write-Host ""
Write-Host "🚀 Starting HealFind AI server..." -ForegroundColor Green
Write-Host "📱 Open your browser and go to: http://localhost:5000" -ForegroundColor Cyan
Write-Host ""

Set-Location backend
python app.py

Read-Host "Press Enter to exit"