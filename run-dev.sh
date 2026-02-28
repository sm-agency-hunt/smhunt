#!/bin/bash

# SMHunt Development Environment Setup Script
# For Windows users: Run this with Git Bash or WSL

echo "========================================="
echo "  SMHunt Development Environment Setup  "
echo "========================================="
echo

# Check if we're in the correct directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

echo "🔄 Setting up development environment..."
echo

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "🔹 Creating virtual environment..."
    python -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔹 Activating virtual environment..."

if [ "$OSTYPE" = "msys" ] || [ "$OSTYPE" = "win32" ]; then
    # Windows Git Bash
    source venv/Scripts/activate
else
    # Linux/Mac
    source venv/bin/activate
fi

# Upgrade pip
echo "🔹 Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements
echo "🔹 Installing Python dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo "✅ Dependencies installed successfully"

# Copy environment file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "🔹 Creating environment configuration..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Environment file created"
        echo "⚠️  Please edit .env with your configuration before running the application"
    else
        echo "⚠️  .env.example file not found. Please create .env manually."
    fi
fi

# Create logs directory
mkdir -p logs
echo "✅ Logs directory created"

echo
echo "========================================="
echo "  Setup Complete!                          "
echo "========================================="
echo
echo "🚀 To start the application:"
echo "   1. Activate virtual environment: source venv/bin/activate"
echo "   2. Run the application: python -m uvicorn simple_app:app --host 0.0.0.0 --port 8000 --reload"
echo "   3. Visit http://localhost:8000/docs for API documentation"
echo ""
echo "   For Windows users:"
echo "   - Use run-app.bat for Command Prompt"
echo "   - Use run-app.ps1 for PowerShell"
echo
echo "📊 Database Migration Note:"
echo "   The application will automatically create database tables"
echo "   and setup the default admin user (admin@smhunt.online/admin123)"
echo "   on first run"