#!/bin/bash
# ========================================================
# setup_and_run.sh
# A script to set up a Python virtual environment,
# install dependencies, and run the Streamlit app.
# ========================================================

# --- Step 0: Variables ---
APP_NAME="main.py"       # Change if your app filename is different
VENV_DIR=".venv"         # Virtual environment folder

# --- Step 1: Check Python installation ---
if ! command -v python3 &> /dev/null; then
    echo "Python3 not found. Please install Python 3.10+."
    exit 1
fi

# --- Step 2: Create virtual environment if missing ---
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
fi

# --- Step 3: Activate virtual environment ---
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# --- Step 4: Upgrade pip ---
echo "Upgrading pip..."
pip install --upgrade pip

# --- Step 5: Install dependencies ---
echo "Installing required libraries..."
pip install --upgrade streamlit openai

# --- Step 6: Run Streamlit app ---
echo "Launching Streamlit app..."
streamlit run "$APP_NAME"

# --- Step 7: Deactivate virtual environment on exit ---
deactivate

