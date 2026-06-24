#!/usr/bin/env bash
# One command to update the live lookbook.
# Usage:  ./publish.sh
set -e
cd "$(dirname "$0")"

echo "▶ Building gallery from your photos…"
python3 build.py

echo "▶ Publishing to the web…"
git add -A
if git diff --cached --quiet; then
  echo "Nothing changed — already up to date."
  exit 0
fi
git commit -m "Update lookbook ($(date '+%Y-%m-%d %H:%M'))"
git push

echo ""
echo "✓ Done. Your changes are live in ~1 minute at:"
echo "   https://sleek-mx.github.io/sleek-lookbook/"
