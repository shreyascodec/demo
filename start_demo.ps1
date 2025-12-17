# LMS Demo Startup Script for Windows
# Run this script to start the demo

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Lab Management System - Demo Startup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Python not found. Please install Python 3.8+ first." -ForegroundColor Red
    exit 1
}

# Check if requirements are installed
Write-Host ""
Write-Host "Checking dependencies..." -ForegroundColor Yellow

$streamlitInstalled = python -c "import streamlit" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies already installed" -ForegroundColor Green
} else {
    Write-Host "! Installing required dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
}

# Start Streamlit
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting LMS Demo..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "The demo will open in your browser automatically." -ForegroundColor Green
Write-Host "If it doesn't, navigate to: http://localhost:8501" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

streamlit run app.py

