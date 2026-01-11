#!/bin/bash
set -e

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed. Please install it first (https://github.com/astral-sh/uv)."
    exit 1
fi

echo "Creating virtual environment and syncing dependencies..."
uv sync

echo "Installing project in editable mode..."
uv pip install -e .

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "env variables not found. Please create a .env file with the following variables:"
    echo "GEMINI_API_KEY"
    exit 1
fi

echo ""
echo "Setup complete! ✅"
echo "To actiavte the environment, run:"
echo "source .venv/bin/activate"
