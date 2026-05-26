from app.core.database import Base, SessionLocal, engine
from app.models import Order, OrderItem, OrderStatus, OrderTimeline
from random import choice, uniform
Base.metadata.create_all(bind=engine, checkfirst=True)
db=SessionLocal()
statuses=list(OrderStatus)
if db.query(Order).count() < 20:
    for i in range(20):
        subtotal=round(uniform(80,1200),2); tax=round(subtotal*.18,2); shipping=0 if subtotal>250 else 9.99
        order=Order(user_id='demo-customer' if i%2 else 'customer-2', customer_email=f'customer{i}@example.com', status=choice(statuses), subtotal=subtotal, tax=tax, shipping_fee=shipping, total=round(subtotal+tax+shipping,2), shipping_address={'city':'Nagpur','line1':'Astra Tower','postal':'440001'})
        db.add(order); db.flush()
        db.add(OrderItem(order_id=order.id, product_id=f'product-{i}', title=f'Astra Product {i}', unit_price=round(subtotal/2,2), quantity=2, line_total=subtotal))
        db.add(OrderTimeline(order_id=order.id, status=order.status, message=f'Seeded order in {order.status.value}', actor_id='seed'))
    db.commit()
db.close(); print('Seeded 20 orders')
