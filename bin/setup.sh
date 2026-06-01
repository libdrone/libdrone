#!/usr/bin/env bash
# libdrone 3.0.0 — environment setup
# Run once after cloning the repo.
# Usage: bash bin/setup.sh

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$REPO_ROOT/.venv"

echo "libdrone — setting up Python environment"
echo "Repo: $REPO_ROOT"

# Check Python version
PYTHON=$(command -v python3 || command -v python)
if [ -z "$PYTHON" ]; then
    echo "ERROR: python3 not found. Install Python 3.9+ and retry."
    exit 1
fi

PY_VERSION=$($PYTHON -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Python: $PY_VERSION at $PYTHON"

# Create venv
if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment already exists at .venv — skipping creation"
else
    echo "Creating virtual environment at .venv"
    $PYTHON -m venv "$VENV_DIR"
fi

# Activate and install
source "$VENV_DIR/bin/activate"
echo "Installing dependencies from requirements.txt"
pip install --quiet --upgrade pip
pip install --quiet -r "$REPO_ROOT/requirements.txt"

echo ""
echo "Setup complete."
echo ""
echo "To activate the environment:"
echo "  source .venv/bin/activate          # Linux / macOS"
echo "  .venv\\Scripts\\activate             # Windows"
echo ""
echo "To validate a single article:"
echo "  python3 bin/validate_corpus.py articles/domain/article.md"
echo ""
echo "To validate the full corpus:"
echo "  python3 bin/validate_corpus.py articles/"
echo ""
echo "To validate with connection graph integrity:"
echo "  python3 bin/validate_corpus.py articles/ --graph"
