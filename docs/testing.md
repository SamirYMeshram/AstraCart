# Testing

The repository includes service-level tests and gateway tests. Tests cover health endpoints, registration/login/refresh, product creation/search, cart view, orders list, payment initiation, notification creation, gateway health and route fallback.

Run:

```bash
make test
```

The test script first runs structural validation and then executes Pytest inside service containers.

Recommended future test expansion:

- Contract tests between gateway and services.
- End-to-end create-order and payment-success flow.
- Load tests for Redis rate limiting.
- Frontend component tests for chart and pipeline interactions.
