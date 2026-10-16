#!/usr/bin/env bash
# Build the Impulse Learning Center A1 Vocabulary Book PDF.
# Two passes: the first finds the page each unit starts on, the second
# writes those page numbers into the contents page.
set -euo pipefail
cd "$(dirname "$0")"
python3 scripts/build_html.py
node scripts/render.js
python3 scripts/build_html.py dist/pages.json
node scripts/render.js
pdfunite dist/front.pdf dist/body.pdf "dist/Impulse_A1_Vocabulary_Book.pdf"
rm -f dist/front.pdf dist/body.pdf dist/book.pdf
echo "Done: dist/Impulse_A1_Vocabulary_Book.pdf"
