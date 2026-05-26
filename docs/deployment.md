# Deployment

The included Docker Compose file is optimized for local development and portfolio demos. For production, use managed PostgreSQL, managed Redis, separate secrets management, TLS termination, observability and autoscaling.

## Production hardening checklist

- Rotate `JWT_SECRET_KEY` using a real secret manager.
- Use separate database users per service.
- Enable structured JSON logs and OpenTelemetry traces.
- Put the gateway behind a TLS-enabled reverse proxy.
- Add idempotency keys for order and payment mutation endpoints.
- Add backup policies for all service databases.
- Deploy Celery workers separately from API replicas.
