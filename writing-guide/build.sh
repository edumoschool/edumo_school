#!/usr/bin/env bash
# Build "Write it Right!" (playful Multilevel writing guide): HTML -> PDF -> merged with cover.
set -euo pipefail
cd "$(dirname "$0")"
python3 scripts/build.py
NODE_PATH=/opt/node22/lib/node_modules node scripts/render.js
python3 scripts/merge.py
rm -f dist/interior.pdf dist/cover.pdf
