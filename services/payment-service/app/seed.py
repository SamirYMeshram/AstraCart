from random import choice, uniform
from app.core.database import Base, SessionLocal, engine
from app.models import PaymentStatus
from app.repositories import PaymentRepository
from app.schemas import PaymentInitiate
Base.metadata.create_all(bind=engine, checkfirst=True)
db=SessionLocal(); repo=PaymentRepository(db)
if len(repo.history()) < 20:
    statuses=[PaymentStatus.SUCCESS,PaymentStatus.SUCCESS,PaymentStatus.FAILED,PaymentStatus.REFUNDED,PaymentStatus.INITIATED]
    for i in range(20):
        p=repo.create('demo-customer' if i%2 else 'customer-2', PaymentInitiate(order_id=f'order-{i}', amount=round(uniform(120,1500),2), currency='INR'))
        repo.mark(p, choice(statuses), {'seed': True})
db.close(); print('Seeded 20 payments')
