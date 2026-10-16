#!/usr/bin/env bash
# Build the Impulse Learning Center A2 Writing Book.
set -euo pipefail
cd "$(dirname "$0")"
python3 scripts/build.py
node scripts/render.js
