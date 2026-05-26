from fastapi import HTTPException
import httpx
from app.core.config import get_settings
from app.models import OrderStatus
from app.repositories import OrderRepository
class OrderService:
    def __init__(self, repo: OrderRepository): self.repo=repo
    async def create_from_cart(self, user_id: str, payload) -> object:
        settings=get_settings()
        async with httpx.AsyncClient(timeout=8) as client:
            cart_response=await client.get(f'{settings.cart_service_url}/internal/cart/{user_id}')
        if cart_response.status_code != 200: raise HTTPException(status_code=503, detail='Cart service unavailable')
        cart=cart_response.json()['data']
        if not cart['items']: raise HTTPException(status_code=409, detail='Cannot create order from empty cart')
        if not cart['stock_valid']: raise HTTPException(status_code=409, detail='Cart contains invalid stock levels')
        order=self.repo.create(user_id, cart, payload.shipping_address, payload.customer_email)
        async with httpx.AsyncClient(timeout=5) as client:
            for item in cart['items']:
                await client.post(f"{settings.product_service_url}/internal/products/{item['product_id']}/decrement-stock", json={'quantity': item['quantity'], 'reason': 'order_created'})
            await client.delete(f'{settings.cart_service_url}/cart/clear', headers={'X-User-Id': user_id})
        return order
