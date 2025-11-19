#!/usr/bin/env bash
set -euo pipefail

if command -v black >/dev/null 2>&1; then
  black optimizer tests
fi

if command -v isort >/dev/null 2>&1; then
  isort optimizer tests
fi

if command -v terraform >/dev/null 2>&1; then
  find blueprints/terraform -name '*.tf' -print0 | xargs -0 -r terraform fmt
fi
