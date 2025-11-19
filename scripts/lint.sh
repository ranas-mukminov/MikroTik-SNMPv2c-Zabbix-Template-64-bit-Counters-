#!/usr/bin/env bash
set -euo pipefail

echo "[lint] Python formatting"
if command -v ruff >/dev/null 2>&1; then
  ruff check optimizer tests
else
  echo "ruff not installed, skipping"
fi

if command -v black >/dev/null 2>&1; then
  black --check optimizer tests
else
  echo "black not installed, skipping"
fi

if command -v yamllint >/dev/null 2>&1; then
  yamllint config blueprints/**/*.yml blueprints/**/*.yaml || true
else
  echo "yamllint not installed, skipping"
fi

if command -v terraform >/dev/null 2>&1; then
  find blueprints/terraform -name '*.tf' -print0 | xargs -0 -r terraform fmt -check
else
  echo "terraform not installed, skipping fmt"
fi

echo "[lint] done"
