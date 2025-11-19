#!/usr/bin/env bash
set -euo pipefail

if command -v pip-audit >/dev/null 2>&1; then
  pip-audit
else
  echo "pip-audit not installed, skipping"
fi

if command -v bandit >/dev/null 2>&1; then
  bandit -r optimizer
else
  echo "bandit not installed, skipping"
fi
