#!/usr/bin/env bash
# Build the Multilevel Mock Tests book: interior (2 columns, A4) + cover, merged into one PDF.
set -euo pipefail
cd "$(dirname "$0")"
python3 scripts/build.py
START_PAGE=1 node scripts/render.js
python3 scripts/cover.py
node scripts/cover_render.js
python3 scripts/merge.py
rm -f dist/cover_pages.html dist/cover_spread.html
