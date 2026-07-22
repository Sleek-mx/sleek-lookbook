#!/usr/bin/env bash
# One command to update the live website + look book.
# Usage:  ./publish.sh
set -e
cd "$(dirname "$0")"

# ── first run sets up its own private Python (the Mac's python3 has no Pillow) ──
if [ ! -x ".venv/bin/python" ]; then
  echo "▶ First run — setting up the photo tools (about a minute)…"
  PY="$(command -v python3.14 || command -v python3.13 || command -v python3.12 || command -v python3.11 || command -v python3)"
  "$PY" -m venv .venv
  .venv/bin/pip install --quiet --upgrade pip
  .venv/bin/pip install --quiet Pillow pillow-heif
fi

echo "▶ Building gallery from your photos…"
.venv/bin/python build.py

echo "▶ Publishing to the web…"
git add -A
if git diff --cached --quiet; then
  echo "Nothing changed — already up to date."
  exit 0
fi
git commit -m "Update site ($(date '+%Y-%m-%d %H:%M'))"
git push

echo ""
echo "✓ Done. Your changes are live in ~1 minute at:"
echo "   https://sleek-mx.github.io/sleek-lookbook/"
