#!/usr/bin/env bash
# Build Impulse Learning Center vocabulary books.
# Usage: ./build.sh [A1|A2 ...]   (default: all levels)
# Two passes per level: the first finds the page each unit starts on, the
# second writes those page numbers into the contents page.
set -euo pipefail
cd "$(dirname "$0")"
levels=("$@"); [ ${#levels[@]} -eq 0 ] && levels=(A1 A2)
for L in "${levels[@]}"; do
  d="dist/${L,,}"
  python3 scripts/build_html.py "$L"
  node scripts/render.js "$L" >/dev/null
  python3 scripts/build_html.py "$L" "$d/pages.json"
  node scripts/render.js "$L" >/dev/null
  pdfunite "$d/front.pdf" "$d/body.pdf" "dist/Impulse_${L}_Vocabulary_Book.pdf"
  rm -f "$d/front.pdf" "$d/body.pdf"
  echo "Done: dist/Impulse_${L}_Vocabulary_Book.pdf ($(pdfinfo "dist/Impulse_${L}_Vocabulary_Book.pdf" | awk '/Pages/{print $2}') pages)"
done
