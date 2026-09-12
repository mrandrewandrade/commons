#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-site/index.qmd}"
PORT="${PORT:-6590}"

echo "Fast Quarto preview: ${TARGET} on port ${PORT}"
echo "Use: bash scripts/preview.sh site when you explicitly want a full-site preview."

exec quarto preview "${TARGET}" --port "${PORT}"
