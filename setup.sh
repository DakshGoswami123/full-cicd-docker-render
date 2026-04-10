#!/usr/bin/env bash
set -e

echo "Creating Python virtual environment..."
python -m venv .venv

echo "Activating virtual environment..."
source .venv/Scripts/activate 2>/dev/null || source .venv/bin/activate

echo "Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Running automated tests..."
pytest AutoTesting -q

echo ""
echo "Setup complete."
echo "Run locally with: python -m flask --app app.main run --host=0.0.0.0 --port=5000"
echo "Or with Docker: docker compose up --build"

