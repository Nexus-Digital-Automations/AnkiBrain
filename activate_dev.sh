#!/bin/bash
# AnkiBrain Development Environment Activation Script
# Generated on 2025-09-13

echo "🚀 Activating AnkiBrain Development Environment..."

# Activate virtual environment
source user_files/venv/bin/activate

# Set environment variables
export ANKIBRAIN_DEV=1
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Verify activation
echo "✅ Virtual environment activated"
echo "📍 Python: $(which python)"
echo "📦 Pip: $(which pip)"
echo "🏠 Project root: $(pwd)"
echo ""
echo "🧠 AnkiBrain development environment ready!"
echo ""
echo "To run development commands:"
echo "  python -m ruff check .                    # Run linting"
echo "  python -c 'from performance_logger import get_performance_logger; print("Logger works!")'"
echo ""
echo "To deactivate: deactivate"
