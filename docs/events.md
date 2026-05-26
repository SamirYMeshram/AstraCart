# Events and Async Workflows

AstraCart currently models async workflows with Celery tasks and HTTP service calls. The event model is intentionally simple and ready to evolve toward a message bus or transactional outbox.

## Supported events

- USER_REGISTERED
- ORDER_PLACED
- PAYMENT_SUCCESSFUL
- ORDER_SHIPPED
- ORDER_DELIVERED
- REFUND_PROCESSED

## Order flow

1. Customer adds products to cart.
2. Cart service validates product stock.
3. Order service creates a PENDING order from cart lines.
4. Product service decrements inventory.
5. Payment service initiates and confirms mock payment.
6. Payment success moves the order to PAID.
7. Notification service records confirmation messages.
8. Frontend dashboard visualizes analytics and system health.
