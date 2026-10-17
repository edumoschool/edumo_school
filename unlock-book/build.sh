#!/usr/bin/env bash
# Build the whole Unlock 5 book: Units 1-3 (original PDFs + extra pages) and Units 4-10, merged into one PDF.
set -euo pipefail
cd "$(dirname "$0")"
python3 scripts/build.py --front
START_PAGE=1 INPUT=front.html node scripts/render.js dist/front.pdf
python3 scripts/build.py --extra
START_PAGE=41 INPUT=extra.html node scripts/render.js dist/Unit3_extra.pdf
EXTRA=$(python3 -c "from pypdf import PdfReader; print(len(PdfReader('dist/Unit3_extra.pdf').pages))")
python3 scripts/build.py
START_PAGE=$((41 + EXTRA)) node scripts/render.js
python3 scripts/merge.py
