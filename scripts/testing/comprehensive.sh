#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
quarto render site
exec python scripts/check_commons.py --rendered
