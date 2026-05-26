from datetime import datetime, timezone
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from app.models import CartItem
class CartRepository:
    def __init__(self, db: Session): self.db=db
    def items(self, user_id: str) -> list[CartItem]: return list(self.db.scalars(select(CartItem).where(CartItem.user_id==user_id).order_by(CartItem.created_at)))
    def get(self, item_id: str, user_id: str) -> CartItem | None: return self.db.scalar(select(CartItem).where(CartItem.id==item_id, CartItem.user_id==user_id))
    def get_by_product(self, product_id: str, user_id: str) -> CartItem | None: return self.db.scalar(select(CartItem).where(CartItem.product_id==product_id, CartItem.user_id==user_id))
    def upsert(self, user_id: str, product: dict, quantity: int) -> CartItem:
        existing = self.get_by_product(product['id'], user_id)
        price = product.get('discount_price') or product['price']
        if existing:
            existing.quantity += quantity; existing.stock_at_add = product['stock_quantity']; existing.unit_price = price
            item = existing
        else:
            item = CartItem(user_id=user_id, product_id=product['id'], title=product['title'], unit_price=price, quantity=quantity, stock_at_add=product['stock_quantity'], thumbnail=(product.get('images') or [None])[0])
            self.db.add(item)
        self.db.commit(); self.db.refresh(item); return item
    def update_qty(self, item: CartItem, quantity: int) -> CartItem:
        item.quantity=quantity; self.db.commit(); self.db.refresh(item); return item
    def delete(self, item: CartItem): self.db.delete(item); self.db.commit()
    def clear(self, user_id: str): self.db.execute(delete(CartItem).where(CartItem.user_id==user_id)); self.db.commit()
    def cleanup_expired(self) -> int:
        res = self.db.execute(delete(CartItem).where(CartItem.expires_at < datetime.now(timezone.utc))); self.db.commit(); return res.rowcount or 0
