#!/usr/bin/env bash
# Wrapper to run all static checks for MikroTik Zabbix templates.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "[run_checks] Missing python3 interpreter (set PYTHON_BIN to override)." >&2
  exit 1
fi

cd "$ROOT_DIR/tests"

echo "==============================================="
echo " MikroTik Zabbix Template Static Validation"
echo "==============================================="

set +e
"$PYTHON_BIN" validate_xml.py --all
STATUS=$?
set -e

if [[ $STATUS -ne 0 ]]; then
  echo "[run_checks] Validation failed with status $STATUS" >&2
  exit $STATUS
fi

echo "\nAll template validation checks passed."
