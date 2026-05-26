# Architecture

AstraCart uses a clean microservices architecture. Each domain service owns its FastAPI application, SQLAlchemy models, repository layer, service layer, schemas, tests, Dockerfile, requirements and Alembic migration wiring.

## Runtime flow

1. Clients call the API Gateway.
2. The gateway decodes JWTs, applies role-aware Redis rate limits, logs timing, forwards actor headers and proxies to the target service.
3. Services persist data in isolated PostgreSQL databases.
4. Redis powers gateway rate limiting and Celery brokers.
5. Celery workers process notifications, cart cleanup and scheduled sales reports.

## Service boundaries

- User Service owns identity, authentication, refresh tokens and RBAC.
- Product Service owns catalog, categories, seller ownership and stock.
- Cart Service owns user cart state and stock-aware subtotal calculation.
- Order Service owns order creation, status transitions and timeline auditing.
- Payment Service owns mock transactions, receipts and refunds.
- Notification Service owns email/SMS/in-app notification records and dispatch tasks.

## Gateway limits

- Anonymous: 30 requests/minute.
- Customer, seller and support: 100 requests/minute.
- Admin: 300 requests/minute.
