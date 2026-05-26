#!/usr/bin/env bash
set -euo pipefail
python scripts/validate_project.py
for svc in services/*-service; do
  if [ -d "$svc/tests" ]; then
    echo "Running tests for $svc"
    docker compose run --rm "$(basename "$svc")" pytest -q
  fi
done
