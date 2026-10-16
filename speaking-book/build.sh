#!/usr/bin/env bash
# Build the Impulse Learning Center A1 Speaking Book PDF.
set -euo pipefail
cd "$(dirname "$0")"
python3 scripts/build.py
node scripts/render.js
