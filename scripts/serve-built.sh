#!/usr/bin/env bash
set -euo pipefail

PORT="${PORT:-6590}"
SITE_DIR="${SITE_DIR:-site/_site}"

if [ ! -d "${SITE_DIR}" ]; then
  echo "${SITE_DIR} does not exist. Build the site first with: quarto render site"
  exit 1
fi

echo "Serving the already-built site from ${SITE_DIR} on port ${PORT}."
echo "This does not watch files or rebuild when source files change."

exec python -m http.server "${PORT}" --directory "${SITE_DIR}"
