from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.models import Order, OrderItem, OrderStatus, OrderTimeline
class OrderRepository:
    def __init__(self, db: Session): self.db=db
    def list(self, user_id: str | None=None, limit: int=100) -> list[Order]:
        stmt=select(Order).options(selectinload(Order.items), selectinload(Order.timeline)).order_by(Order.created_at.desc()).limit(limit)
        if user_id: stmt=stmt.where(Order.user_id==user_id)
        return list(self.db.scalars(stmt))
    def get(self, order_id: str) -> Order | None:
        return self.db.scalar(select(Order).options(selectinload(Order.items), selectinload(Order.timeline)).where(Order.id==order_id))
    def create(self, user_id: str, cart: dict, shipping_address: dict, customer_email: str | None) -> Order:
        subtotal=round(cart['subtotal'],2); tax=round(subtotal*0.18,2); shipping=0 if subtotal>250 else 9.99; total=round(subtotal+tax+shipping,2)
        order=Order(user_id=user_id, customer_email=customer_email, subtotal=subtotal, tax=tax, shipping_fee=shipping, total=total, shipping_address=shipping_address)
        self.db.add(order); self.db.flush()
        for i in cart['items']:
            self.db.add(OrderItem(order_id=order.id, product_id=i['product_id'], title=i['title'], unit_price=i['unit_price'], quantity=i['quantity'], line_total=i['line_total']))
        self.db.add(OrderTimeline(order_id=order.id, status=OrderStatus.PENDING, message='Order created and awaiting payment', actor_id=user_id))
        self.db.commit(); self.db.refresh(order); return self.get(order.id)
    def status(self, order: Order, status: OrderStatus, actor_id: str | None, message: str | None=None) -> Order:
        order.status=status; self.db.add(OrderTimeline(order_id=order.id, status=status, message=message or f'Order moved to {status.value}', actor_id=actor_id))
        self.db.commit(); return self.get(order.id)
