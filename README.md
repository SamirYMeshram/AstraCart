# AstraCart — Enterprise Microservices E-Commerce Platform

AstraCart is a production-style e-commerce platform built as a microservices system with a premium Next.js control plane. It includes independent FastAPI services, PostgreSQL databases, Redis-backed rate limiting, Celery workers, JWT authentication, RBAC, seed data, API tests, Docker Compose, and a futuristic SaaS dashboard.

## What is included

- API Gateway with JWT verification, service routing, Redis rate limiting, request timing headers, health aggregation, and consistent API response envelopes.
- User Service with registration, login, refresh tokens, bcrypt password hashing, profile management, admin user listing, and role updates.
- Product Service with categories, catalog search, seller product management, inventory decrementing, low-stock detection, and archival deletes.
- Cart Service with add/update/remove/clear, subtotal calculation, stock validation and Celery-powered expired-cart cleanup.
- Order Service with create-from-cart flow, order history, admin management, status lifecycle, cancellation, order items and timeline audit events.
- Payment Service with mock gateway initiation, success/failure simulation, refund flow, receipts and transaction history.
- Notification Service with mock email/SMS/in-app notifications, read states and Celery dispatch tasks.
- Premium frontend with landing page, admin dashboard, product management, order pipeline, storefront, system architecture map, notification center and analytics.

## Tech stack

Backend: Python 3.11, FastAPI, SQLAlchemy 2.0, Pydantic, Alembic, PostgreSQL, Redis, Celery, JWT, Passlib/Bcrypt, Pytest, HTTPX.  
Frontend: Next.js, TypeScript, Tailwind CSS, Framer Motion, Recharts, Lucide Icons.  
DevOps: Docker, Docker Compose, Makefile, health checks, seed scripts, migration scripts and validation scripts.

## Demo credentials

| Role | Email | Password |
| --- | --- | --- |
| Admin | admin@astracart.dev | AdminPass123! |
| Seller 1 | seller1@astracart.dev | SellerPass123! |
| Seller 2 | seller2@astracart.dev | SellerPass123! |
| Customer 1 | customer1@astracart.dev | CustomerPass123! |
| Customer 2 | customer2@astracart.dev | CustomerPass123! |
| Support | support@astracart.dev | SupportPass123! |

## Run locally with Docker

```bash
docker compose up --build
make seed
make test
```

Frontend: http://localhost:3000  
API Gateway: http://localhost:8080  
OpenAPI docs through individual services: http://localhost:8001/docs through http://localhost:8006/docs.

## Useful commands

```bash
make up       # build and start all services
make down     # stop containers
make build    # build containers
make logs     # stream logs
make migrate  # run Alembic migrations
make seed     # seed all services
make test     # run validation and service tests
make clean    # remove containers and volumes
```

## Environment variables

Copy `.env.example` to `.env` and change secrets before production-like use. The sample file intentionally contains no real secrets.

## Screenshots section

The frontend is designed around dark luxury SaaS visuals: glassmorphism panels, neon aurora gradients, animated architecture nodes, floating metric cards, responsive layouts, chart-heavy dashboards, and motion-enhanced interactions. Capture screenshots from `/`, `/dashboard`, `/store`, `/architecture`, and `/analytics` after running Docker.

## Troubleshooting

- If services start before PostgreSQL is ready, run `docker compose restart <service-name>`.
- If migrations are already applied, Alembic migration scripts use `checkfirst=True` and are safe to re-run.
- If the frontend cannot reach the backend, confirm `NEXT_PUBLIC_API_BASE_URL=http://localhost:8080`.
- If Redis is unavailable, gateway rate limiting falls back to an in-memory limiter for local tests.

## Future improvements

- Replace mock payments with Stripe/Razorpay adapters.
- Add OpenTelemetry tracing, Prometheus metrics and Grafana dashboards.
- Split event contracts into a shared schema registry.
- Add Kubernetes manifests and blue-green deployment examples.
- Add transactional outbox and idempotency keys for order/payment workflows.
