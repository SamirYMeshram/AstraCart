#!/usr/bin/env bash
set -euo pipefail
services=(user-service product-service cart-service order-service payment-service notification-service)
for svc in "${services[@]}"; do
  echo "Seeding $svc"
  docker compose run --rm "$svc" python -m app.seed
done
