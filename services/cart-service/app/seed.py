from app.core.database import Base, SessionLocal, engine
from app.models import CartItem
Base.metadata.create_all(bind=engine, checkfirst=True)
db=SessionLocal()
if not db.query(CartItem).first():
    db.add(CartItem(user_id='demo-customer', product_id='seed-product', title='Seed Aurora Headphones', unit_price=149.99, quantity=2, stock_at_add=12, thumbnail='https://images.unsplash.com/photo-1505740420928-5e560c06d30e'))
    db.commit()
db.close(); print('Seeded cart service')
