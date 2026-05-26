# API Reference

All normal responses use:

```json
{ "success": true, "message": "string", "data": {} }
```

Errors use:

```json
{ "success": false, "message": "string", "error": "string" }
```

## User Service

- POST `/auth/register`
- POST `/auth/login`
- POST `/auth/refresh`
- GET `/users/me`
- PATCH `/users/me`
- GET `/admin/users`
- PATCH `/admin/users/{user_id}/role`

## Product Service

- GET `/products`
- GET `/products/{product_id}`
- POST `/products`
- PATCH `/products/{product_id}`
- DELETE `/products/{product_id}`
- GET `/categories`
- POST `/categories`
- GET `/products/search`
- GET `/inventory/low-stock`
- POST `/internal/products/{product_id}/decrement-stock`

## Cart Service

- GET `/cart`
- POST `/cart/items`
- PATCH `/cart/items/{item_id}`
- DELETE `/cart/items/{item_id}`
- DELETE `/cart/clear`

## Order Service

- POST `/orders`
- GET `/orders`
- GET `/orders/{order_id}`
- PATCH `/orders/{order_id}/status`
- POST `/orders/{order_id}/cancel`
- GET `/admin/orders`

## Payment Service

- POST `/payments/initiate`
- POST `/payments/{payment_id}/confirm`
- GET `/payments/{payment_id}`
- GET `/payments`
- POST `/payments/{payment_id}/refund`

## Notification Service

- POST `/notifications`
- GET `/notifications`
- PATCH `/notifications/{notification_id}/read`
