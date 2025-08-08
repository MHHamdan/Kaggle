#!/bin/bash
# GPT-OSS Red-Teaming Environment Activation Script
# This script activates the virtual environment and sets up the development environment

echo "🚀 Activating GPT-OSS Red-Teaming Environment..."

# Navigate to project directory
cd "$(dirname "$0")"

# Activate virtual environment
if [ -d "gpt-oss" ]; then
    source gpt-oss/bin/activate
    echo "✅ Virtual environment 'gpt-oss' activated"
else
    echo "❌ Virtual environment 'gpt-oss' not found!"
    echo "Please run: python -m venv gpt-oss"
    exit 1
fi

# Check if environment variables are set
if [ -f ".env" ]; then
    echo "✅ Environment variables loaded from .env"
else
    echo "⚠️  No .env file found. Copy env.example to .env and configure your API keys"
fi

# Display project info
echo ""
echo "📊 GPT-OSS-20B Red-Teaming Challenge Environment"
echo "=============================================="
echo "🔗 GitHub: https://github.com/MHHamdan/Kaggle"
echo "📁 Project: gpt-oss-20b-red-teaming"
echo "🐍 Python: $(python --version)"
echo "📦 Virtual Env: gpt-oss"
echo ""

# Check key dependencies
echo "🔍 Checking key dependencies..."
python -c "import openai; print('✅ OpenAI library available')" 2>/dev/null || echo "❌ OpenAI library not found"
python -c "import transformers; print('✅ Transformers library available')" 2>/dev/null || echo "❌ Transformers library not found"
python -c "import jupyter; print('✅ Jupyter available')" 2>/dev/null || echo "❌ Jupyter not found"

echo ""
echo "🎯 Ready for red-teaming! Available commands:"
echo "  jupyter notebook          # Start Jupyter for interactive testing"
echo "  python src/models/...      # Run model interaction scripts"
echo "  pytest tests/             # Run test suite"
echo ""
echo "📚 Quick start:"
echo "  1. Set your OpenAI API key in .env file"
echo "  2. Open notebooks/01_model_exploration.ipynb"
echo "  3. Begin systematic vulnerability testing"
echo ""

# Keep shell active in the virtual environment
exec "$SHELL"
