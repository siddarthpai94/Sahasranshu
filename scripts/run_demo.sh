#!/bin/bash

# Ensure we are in the project root
cd "$(dirname "$0")/.."
set -e

# Check for API Key
if [ -z "$GEMINI_API_KEY" ]; then
    echo "Error: GEMINI_API_KEY is not set."
    echo "Please export your API key first:"
    echo "  export GEMINI_API_KEY='your-api-key-here'"
    exit 1
fi

echo "Running Sahasranshu on Dec 2024 FOMC Statement..."
echo "Note: This will automatically compare it with the Nov 2024 statement if found."

# Run the pipeline
PYTHONPATH=src .venv/bin/python run_one.py data/US/FED/2024/Dec/manifests/2024-12-18_FOMC_Statement.json --use-llm

echo "Done."
echo "Check the 'processed' directory for the generated memo."
