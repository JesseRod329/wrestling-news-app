#!/bin/bash
# A script to set up and run the Real Wrestling News app.

# --- Configuration ---
VENV_DIR=".venv"
REQUIREMENTS_FILE="requirements.txt"
UVICORN_COMMAND="uvicorn app.main:app --reload"

# --- Logic ---
echo "🚀 Starting Real Wrestling News setup..."

# Check if the virtual environment directory exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Creating one at '$VENV_DIR'..."
    python -m venv $VENV_DIR
fi

# Activate the virtual environment (for this script session)
if [ -f "$VENV_DIR/bin/activate" ]; then
  # Linux/macOS
  source "$VENV_DIR/bin/activate"
elif [ -f "$VENV_DIR/Scripts/activate" ]; then
  # Windows Git Bash
  source "$VENV_DIR/Scripts/activate"
fi

echo "✅ Virtual environment activated."

# Install/update dependencies
echo "📦 Installing dependencies from $REQUIREMENTS_FILE..."
pip install -r $REQUIREMENTS_FILE
echo "✅ Dependencies are up to date."

# Run the Uvicorn server
echo "🔥 Launching the FastAPI server..."
echo "UI:  http://localhost:8000/static/index.html"
echo "API: http://localhost:8000/docs"

exec $UVICORN_COMMAND


