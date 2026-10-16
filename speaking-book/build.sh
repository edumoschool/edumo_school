#!/usr/bin/env bash
# Build the Impulse Learning Center speaking books (A1, A2 and B1).
set -euo pipefail
cd "$(dirname "$0")/scripts"
python3 build.py && node render.js speaking-book.html Impulse_A1_Speaking_Book.pdf
python3 build_a2.py && node render.js a2-speaking-book.html Impulse_A2_Speaking_Book.pdf
python3 build_b1.py && node render.js b1-speaking-book.html Impulse_B1_Speaking_Book.pdf
