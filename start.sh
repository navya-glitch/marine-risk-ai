#!/bin/bash
set -e

echo "🚢 Marine Risk AI - Startup Script"
echo "=================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "⚠️ Ollama is not installed. Please install Ollama first:"
    echo "   Visit https://ollama.ai for installation instructions"
    exit 1
fi

# Check if Ollama model is available
echo "Checking Ollama model..."
if ! ollama list | grep -q "qwen2.5:3b"; then
    echo "⚠️ Ollama model 'qwen2.5:3b' not found. Pulling now..."
    ollama pull qwen2.5:3b
fi

echo "✅ Ollama model ready"
echo ""

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "✅ .env file created"
fi

# Start services
echo "Starting services with Docker Compose..."
echo ""
docker-compose up --build

echo ""
echo "🎉 Marine Risk AI is running!"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
