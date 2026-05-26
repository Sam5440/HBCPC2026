#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
  python -m venv .venv
fi

if [ -f ".venv/Scripts/activate" ]; then
  # Windows Git Bash / MSYS
  source ".venv/Scripts/activate"
else
  source ".venv/bin/activate"
fi

python -m pip install -r requirements.txt
export FLASK_APP=web.app
python -m flask run --host 127.0.0.1 --port "${PORT:-5000}"
