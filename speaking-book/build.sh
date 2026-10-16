#!/usr/bin/env bash
# Build the Impulse Learning Center speaking books (A1 and A2).
set -euo pipefail
cd "$(dirname "$0")/scripts"
python3 build.py && node render.js speaking-book.html Impulse_A1_Speaking_Book.pdf
python3 build_a2.py && node render.js a2-speaking-book.html Impulse_A2_Speaking_Book.pdf
