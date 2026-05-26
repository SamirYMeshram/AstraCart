from fastapi import HTTPException
import httpx
from app.core.config import get_settings
from app.models import CartItem
from app.repositories import CartRepository

def item_to_dict(i: CartItem) -> dict:
    return {'id':i.id,'user_id':i.user_id,'product_id':i.product_id,'title':i.title,'unit_price':i.unit_price,'quantity':i.quantity,'stock_at_add':i.stock_at_add,'thumbnail':i.thumbnail,'line_total':round(i.unit_price*i.quantity,2)}
class CartService:
    def __init__(self, repo: CartRepository): self.repo=repo
    async def fetch_product(self, product_id: str) -> dict:
        url=f"{get_settings().product_service_url}/products/{product_id}"
        async with httpx.AsyncClient(timeout=5) as client:
            r=await client.get(url)
        if r.status_code!=200: raise HTTPException(status_code=404, detail='Product not found or product service unavailable')
        return r.json()['data']
    async def add(self, user_id: str, product_id: str, qty: int) -> dict:
        product=await self.fetch_product(product_id)
        if product['stock_quantity'] < qty: raise HTTPException(status_code=409, detail='Insufficient stock')
        return item_to_dict(self.repo.upsert(user_id, product, qty))
    def view(self, user_id: str) -> dict:
        items=[item_to_dict(i) for i in self.repo.items(user_id)]
        return {'items':items,'subtotal':round(sum(i['line_total'] for i in items),2),'item_count':sum(i['quantity'] for i in items),'stock_valid':all(i['quantity'] <= i['stock_at_add'] for i in items)}
