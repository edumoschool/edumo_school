#!/usr/bin/env bash
# Build the Impulse Learning Center writing books.
# Usage: ./build.sh [A2|B1 ...]   (default: all levels)
set -euo pipefail
cd "$(dirname "$0")"
levels=("$@"); [ ${#levels[@]} -eq 0 ] && levels=(A2 B1)
for L in "${levels[@]}"; do
  python3 scripts/build.py "$L"
  node scripts/render.js "$L"
done
