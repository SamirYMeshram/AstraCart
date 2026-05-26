# Database Design

AstraCart uses PostgreSQL with isolated databases per service:

- `users_db`
- `products_db`
- `carts_db`
- `orders_db`
- `payments_db`
- `notifications_db`

Each service includes Alembic scaffolding and a first migration that creates SQLAlchemy metadata with `checkfirst=True`. Services also create tables on startup for local developer convenience.

## Main entities

- Users: role, active state, password hash and profile metadata.
- Products: catalog data, seller ownership, status and inventory.
- Cart items: user-specific product lines, quantity and stock snapshot.
- Orders: header, items, totals, shipping address and timeline audit records.
- Payments: transaction amount, status, gateway reference, receipt and metadata.
- Notifications: user, event, channel, read state and metadata.
