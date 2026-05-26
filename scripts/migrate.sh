#!/usr/bin/env bash
set -euo pipefail
services=(user-service product-service cart-service order-service payment-service notification-service)
for svc in "${services[@]}"; do
  echo "Running migrations for $svc"
  docker compose run --rm "$svc" alembic upgrade head
done
