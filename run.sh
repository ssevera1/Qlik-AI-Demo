#!/usr/bin/env bash
echo "============================================"
echo " Qlik Cloud AI/ML Capabilities Demo"
echo "============================================"
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed."
    echo "Install via: brew install python3"
    exit 1
fi

# Install dependencies if needed
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    echo
fi

# Run the app
echo "Starting Streamlit app..."
streamlit run app.py
